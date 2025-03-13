from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from databasefunc import *
from jikan import *
import sqlite3
app = Flask(__name__)
app.secret_key = '<KEY>'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_FILE_DIR'] = '/session'
Session(app)

#Creates database if it does not exist
db = sqlite3.connect('database.db')
db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT)')
db.execute('CREATE TABLE IF NOT EXISTS animes (id INTEGER PRIMARY KEY, name TEXT, image TEXT)')
db.execute('CREATE TABLE IF NOT EXISTS animelists (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, anime_id INTEGER NOT NULL, UNIQUE(user_id, anime_id), FOREIGN KEY(user_id) REFERENCES users(id), FOREIGN KEY(anime_id) REFERENCES animes(id))')
db.commit()
@app.route('/')
def index():
    return render_template('index.html',latest_animes=getLatestAnimes(),top_animes=getTopAnimes())

@app.route('/login', methods=['GET','POST'])
#Logs user in and can be referenced in the future via their id
def login():
    if request.method == 'GET':
        #If user is already logged in
        if session.get('user_id') is not None:
            return redirect('/animelist')
        return render_template('login.html', error='')

    elif request.method == 'POST':
        #Checks if username/password is correct, sends user to their anime-list, else returns a fail code
        username = request.form['username']
        password = request.form['password']

        if loginValid(username, password):
            session['user_id'] = getUserId(username)
            return redirect('/animelist')
        else:
            return render_template('login.html', error='Invalid username or password')


@app.route('/register', methods=['GET','POST'])
#Registers user, id will be automatically created
#Usernames are unique, so will return an error code if given user already exists
def register():
    if request.method == 'GET':
        return render_template('login.html',error='')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if userExists(username):
            return render_template('login.html', error='Username already exists')
        else:
            createUser(username, password)
            return redirect('/login')



@app.route('/logout')
#Logs user out by clearing their session
def logout():
    session.clear()
    return redirect('/')

@app.route('/animelist')
def animelist():
    #If user is not logged in, they will be redirected to the index page
    if session.get('user_id') is None:
        return redirect('/index',latest_animes=getLatestAnimes(),top_animes=getTopAnimes())

    #If user is logged in, they will be able to see their anime list
    animes = getAnimesForUserId(session['user_id'])
    return render_template("animelist.html", animes=animes, username=getUsername(session['user_id']))

@app.route('/search', methods=['GET','POST'])
def search():
    #Returns search results from Jikan API based on user input
    if request.method == 'POST':
        query = request.form['search']
        animes = searchAnimes(query)
        return render_template('search.html',animes=animes)
    else:
        return render_template('search.html', animes=[])

@app.route('/add', methods=['POST'])
def add():
    #Adds anime to user's animelist, then redirects to their animelist
    if request.method == 'POST':
        id = request.form['add']
        anime = createAnime(id)
        insertAnime(session['user_id'], anime)
        return redirect('/animelist')


@app.route('/remove', methods=['POST'])
#Removes anime from user's animelist, then redirects to their animelist
def remove():
    if request.method == 'POST':
        id = request.form['remove']
        deleteAnime(session['user_id'], id)
        return redirect('/animelist')
    else:
        return redirect('/animelist')

if __name__ == '__main__':
    app.run(debug=True)