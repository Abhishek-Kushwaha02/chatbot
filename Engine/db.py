import csv
import sqlite3

con = sqlite3.connect("dark.db")
cursor = con.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)


query = "INSERT INTO sys_command VALUES (null,'edge', 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')"
cursor.execute(query)
con.commit()

# query = "UPDATE sys_command SET id = 5 WHERE name ='notepad' "
# cursor.execute(query)
# con.commit()

# query = "DELETE from sys_command WHERE name=('Notepad')"
# cursor.execute(query)
# con.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)


# query = "INSERT INTO web_command VALUES (null,'edge', 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')"
# cursor.execute(query)
# con.commit()


# query = "DELETE from web_command WHERE name=('edge')"
# cursor.execute(query)
# con.commit()



cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')


# desired_columns_indices = [0, 18]

# # Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# con.commit()
# con.close()


query = "INSERT INTO contacts VALUES (null,'pawan', '1234567890', 'null')"
cursor.execute(query)
con.commi


# query = "UPDATE contacts SET name = 'sankalp' WHERE id =5"
# cursor.execute(query)
# con.commit()




# query = "DROP table contacts"
# cursor.execute(query)
# con.commit()



# query = 'Sankalp(Lpcps)'
# query = query.strip().lower()

# cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results = cursor.fetchall()
# print(results[0][0])