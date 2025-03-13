import sqlite3
from jikan import Anime
"""
All database related functions are stored in this file

For the database, there are 3 tables, users, animes and animelists
 -Users table stores the user id, username and password, essentially the user details
 -Animes table stores the anime id, name and image, essentially the details of the anime
 -Animelists table stores the combination of user id and anime id, essentially the animes the user has added to their animelist
"""

#Creates an anime object from the database given anime_id
def createAnimeWithDatabaseId(id):
    with sqlite3.connect('database.db') as db:
        db.row_factory = sqlite3.Row
        try:
            anime = dict(db.execute('SELECT * FROM animes WHERE id = ? ', (id,)).fetchone())
        except TypeError:
            print("No such anime in database with given id")
            return

        return Anime(anime['id'], anime['name'], anime['image'])

#Fetches all animes from users animelist
def getAnimesForUserId(id):
    with sqlite3.connect('database.db') as db:
        user_animes_id = db.execute('SELECT anime_id FROM animelists WHERE user_id = ?', (id,)).fetchall()
        user_animes = []
        for anime in user_animes_id:
            id = anime[0]
            user_animes.append(createAnimeWithDatabaseId(id))

        return user_animes

#Adds anime to users animelist and general animes, if anime already exists, it will not be added to the animelist but will update the name and image for internal database
def insertAnime(user_id, anime):
    with sqlite3.connect('database.db') as db:
        db.execute('INSERT INTO animelists(user_id, anime_id) VALUES (?, ?) ON CONFLICT DO NOTHING',
                   (user_id, anime.getId()))
        db.execute('INSERT INTO animes(id, name, image) VALUES (?,?,?) ON CONFLICT (id) DO UPDATE SET name=?, image=?',
                   (anime.getId(), anime.getName(), anime.getImage(),anime.getName(), anime.getImage()))
        db.commit()
    return

#Deletes anime from users animelist
def deleteAnime(user_id, anime_id):
    with sqlite3.connect('database.db') as db:
        db.execute('DELETE FROM animelists WHERE user_id = ? AND anime_id=?', (user_id, anime_id))
        db.commit()
    return

#Checks if username/password is in database
def loginValid(username, password):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        if cursor.fetchone() is None:
            return False
        else:
            return True

#Fetches user id from username
def getUserId(username):
    with sqlite3.connect('database.db') as db:
        id = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()[0]
    return id

#Checks if user exists by checking if username is in database
def userExists(username):
    with sqlite3.connect('database.db') as db:
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if user is None:
        return False
    else:
        return True

#Creates user in database
def createUser(username, password):
    with sqlite3.connect('database.db') as db:
        db.execute('INSERT INTO users(username, password) VALUES (?,?)', (username, password))
        db.commit()
    return

#Fetches username given their id
def getUsername(user_id):
    with sqlite3.connect('database.db') as db:
        username = db.execute('SELECT username FROM users WHERE id = ?', (user_id,)).fetchone()[0]
    return username