import re 
import random 
import sqlite3 

question_pattern = '^Q:.*$'
answer_pattern = '^A:.*$'

jokes = {} 
count = 1

with open('jokes.txt', 'r') as F:
    for line in F: 
        l = line.strip()
        if l == '':
            continue 

        que = re.match(question_pattern, line) 
        ans = re.match(answer_pattern, line)
 
        if que:
            jokes[count] = l 
             
        if ans:
            jokes[count] = jokes[count] + '\n' + l 
            count += 1
                  
total_jokes = count - 1
r = random.randint(0,total_jokes)
print(jokes[r])

# Following Schema has already been created
#sqlite> CREATE TABLE Jokes (
   #...> id INTEGER PRIMARY KEY, 
   #...> qanda TEXT NOT NULL);
#sqlite> .tables 
#Jokes
#sqlite> 

connection = sqlite3.connect("jokes.db") 
cursor = connection.cursor()

# insert all the jokes into the db
for i in jokes.keys():
    cursor.execute("INSERT INTO Jokes VALUES(?, ?)", (i, jokes[i]))

connection.commit()
connection.close() 
