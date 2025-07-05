import eel
import pyaudio
from pipes import quote
import os
import time
import datetime 
import webbrowser
import subprocess
import sqlite3
from Engine.command import speak
from Engine.config import ASSISTANT_NAME
from Engine.helper import extract_yt_term, remove_words
import pywhatkit as kit
import pvporcupine
import struct
import pyautogui
from hugchat import hugchat
import openai
from dotenv  import load_dotenv
import psutil  
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer



con = sqlite3.connect("dark.db")
cursor = con.cursor()



@eel.expose 


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")



def closeCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("close", "")
    query.lower()

    app_name = query.strip()

    if app_name != "":
        try:
            
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                app_path = results[0][0]
                app_base_name = os.path.basename(app_path)
                process_killed = False

                # Iterate over running processes
                for process in psutil.process_iter():
                    try:
                        # Match process executable name with the base name of the app
                        if process.name().lower() == app_base_name.lower():
                            process.terminate()
                            process_killed = True
                            speak(f"Closing {app_name}")
                            break
                    except psutil.NoSuchProcess:
                        pass  # Skip processes that terminate during iteration

                if not process_killed:
                    speak(f"Couldn't find {app_name} running.")
            
            else:
                speak(f"{app_name} is not registered or could not be found.")
        
        except Exception as e:
            speak("Something went wrong")
            print(f"Error: {e}")  # Optional, for debugging


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","grasshopper"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("o")
                time.sleep(2)
                autogui.keyUp("win")

    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


# find contacts(whatsapp)
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 12
        dark_message = "message send successfully to "+name

    elif flag == 'call':        
        target_tab = 7
        message = ''
        dark_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        dark_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(dark_message)

    # chat bot 
def chatBot(query):
    import os
    user_input = query.lower()
    cookie_path = "Engine/cookies.json"
    print("Loading cookies from:", os.path.abspath(cookie_path))
    try:
        chatbot = hugchat.ChatBot(cookie_path=cookie_path)
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)
        response = chatbot.chat(user_input)
        print(response)
        speak(response)
        return response
    except Exception as e:
        print("Error initializing HugChat:", e)
        speak("There was a problem accessing Hugging Face chat.")
        return "Error: " + str(e)



