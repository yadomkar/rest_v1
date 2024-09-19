from bottle import Bottle, request, response, run, template, static_file
from pprint import pprint 
import time 
import algebra 
import os 
import sqlite3 
import random

# file server 


secret = 'CS218 is a Masters class - isntit'

app = Bottle()
 
@app.route('/')
def welcome():
    pprint(dict(request.headers))
    response.set_header('Vary', 'Accept')
    if 'text/html' in request.headers.get('Accept', '*/*'):
        response.content_type = 'text/html' 
        return '<h1>Welcome to CS 218!!!</h1>' 
  
    response.content_type = 'text/plain' 
    return 'hello'

@app.route('/now', method='GET')
def time_server():
    response.content_type = 'text/plain' 
    response.set_header('Cache-Control', 'max-age=3')
    return time.ctime()

@app.route('/joke', method='GET')
def joke_server():
    response.content_type = 'text/plain' 

    # generate a random number between 1 and 163
    # NOTE: DONT HARDCODE numbers in code!!!

    r = random.randint(1, 163)

    connection = sqlite3.connect("jokes.db")
    cursor = connection.cursor() 
    cursor.execute("SELECT * from Jokes WHERE id = ?", (r,))
    (i, joke) = cursor.fetchone()
    connection.close()
    return dict(i=i, joke=joke, service=request.path) 
    
    
@app.route('/upper/<word>', method='GET')
def upper_case_service(word):
    response.content_type = 'text/plain' 
    return word.upper()

@app.route('/prime/<number>', method='GET')
def is_prime(number):
    
    number = int(number)   
    for i in range(2,number):
         if number % i == 0:
             response.content_type = 'text/plain'
             return f'{number} is NOT prime'
    response.content_type = 'text/plain'
    return f'{number} is Prime!!!'


@app.route('/area/circle', method='GET')
def circle_area_service():
    #last_visit = request.get_cookie('last-visit', 'unknown')
    last_visit = request.get_cookie('last-visit', 'unknown', secret=secret)  
    print(f'Last visit {last_visit}')
    response.set_header('Vary', 'Accept')
    #response.set_cookie('last-visit', time.ctime())
    response.set_cookie('last-visit', time.ctime(), secret=secret)
    #pprint(dict(request.query))
    try: 
        radius = float(request.query.get('radius', '0.0'))
    except ValueError as e:
        return e.args[0] 

    area = algebra.area_circle(radius)

    if 'text/html' in request.headers.get('Accept', '*/*'):
        response.content_type = 'text/html' 
        return f'<p>The area of the circle is <em>{area}</em> </p>' 

    return dict(radius=radius, area=area, service=request.path)
    #return 'Test %r ' % area 

file_template = '''\
<h1> List of files in <em> Farm Animals </em> directory </h1>
<hr>
<ol>
  % for file in files:
    <li> <a href= "files/{{file}}"> {{file}} </a></li>
  % end
</ol>
'''
@app.route('/files', method='GET')
def show_files():
    response.set_header('Vary', 'Accept')
    try:
        os.chdir('/home/app/')
    except: 
        print('/home/app directory not present') 

    files = os.listdir('./farm_animals') 
    print(files)

    if 'text/html' not in request.headers.get('Accept', '*/*'):
        return dict(files=files)
    return template(file_template, files=files)

@app.route('/files/<filename>', method='GET')
def serve_one_file(filename):

    try:
        os.chdir('/home/app/')
    except: 
        print('/home/app directory not present') 

    return static_file(filename, './farm_animals')

if __name__ == '__main__': 
    run(app, host='0.0.0.0', port='8088')

#if __name__ == '__main__': 
#    run(host='localhost', port='8080')


