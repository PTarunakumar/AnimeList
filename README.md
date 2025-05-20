# AnimeList
#### Video Demo: 
#### Description: 
Flask Project that allows the user to search for animes they have watched or see the latest/most popular animes. This is achieved by using the Jikan API, a popular API that utilises the MyAnimeList API to gain access to data on animes. The user can then add and track any animes they have previously watched and can also remove them if incorrectly added. Multiple users can access their own indidual animelists via their account.

app.py:
Where the command "flask run" should be used to run the website. Handles the logic of the entire website and should be run when a user enters or leaves a certain page. Some of the functions have been written in different files and then accessed in this file as a module. E.g. createUser() is a function written in databasefunc.py and then accessed in app.py by importing databasefunc.

database.db:
The database for the webstite and stores all data on users, animes previously added by users for quick access and their respective animelists.

databasefunc.py:
Stores all functions that access the database using SqlLite. E.g.:
 - Adding/removing the user to the database. Checking if a user exists.
 - Adding/removing the anime in the users animelist.

jikan.py:
Stores all functions that access the Jikan API, data accessed from the API comes in json so a class Anime has also been created to store relevant data fetched in the API. E.g.:
  -Getting the latest or top animes
  -searching for a particular anime




