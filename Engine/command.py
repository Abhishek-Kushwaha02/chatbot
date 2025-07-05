import webbrowser
import pyttsx3
import speech_recognition as sr
import eel
import time
import datetime
import os
import sys

import wikipedia


def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()


# def wishMe():
#     hour = int(datetime.datetime.now().hour)
#     if hour >= 0 and hour < 12:
#         speak("Good Morning Sir!")
#         print("Good Morning Sir!")

#     elif hour >= 12 and hour < 18:
#         speak("Good Afternoon Sir!")
#         print("Good Afternoon Sir!")

#     else:
#         speak("Good Evening Sir!")
#         print("Good Evening Sir!")

#         time = datetime.datetime.now().strftime('%I:%M %p')
#         speak('the time is' + time)
#         print('the time is' + time)

#     speak("I am Dark your Assistance Sir , How may help you.")
#     print("I am Dark your Assistance Sir , How may help you.") 

def takecommand():
    

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....') 
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    
    return query.lower()


@eel.expose


def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:

        if "open" in query:
            from Engine.feature import openCommand
            openCommand(query)

        elif "close" in query:
            from Engine.feature import closeCommand
            closeCommand(query)

        elif "on youtube" in query:
            from Engine.feature import PlayYoutube
            PlayYoutube(query)

        elif "wikipedia" in query:

            speak("searching wikipedia.....")
            query = query.replace("wikipedia" , "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            print(results)
            speak(results)

        # elif "chrome"in query:
        #     speak("sir, what should i search on chrome")
        #     cm = takecommand().lower()
        #     webbrowser.open(f"{cm}")
        
        elif "search on edge"in query:
            speak("sir, what should i search on edge")
            cm = takecommand().lower()
            webbrowser.open(f"{cm}")


        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from Engine.feature import findContact, whatsApp
            contact_no, name = findContact(query)
            if(contact_no != 0):
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)
           
        else:
            from Engine.feature import chatBot
            chatBot(query)
            # from Engine.feature import ReplyBrain
            # ReplyBrain(query)
    except:
        print("error")
    
    eel.ShowHood()