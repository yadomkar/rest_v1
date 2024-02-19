import random
import sqlite3

r = random.randint(1, 163)
connection = sqlite3.connect("jokes.db") 
cursor = connection.cursor() 


# Following Schema has already been created
#sqlite> CREATE TABLE Jokes (
   #...> id INTEGER PRIMARY KEY, 
   #...> qanda TEXT NOT NULL);
#sqlite> .tables 
#Jokes
#sqlite> 


cursor.execute("SELECT * FROM Jokes WHERE id = ?", (r,))
(i, joke) = cursor.fetchone()

print({'id': i, 'joke': joke})
connection.close()

