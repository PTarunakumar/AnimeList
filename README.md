# AnimeList

#### Video Demo:
(Add link to video demo here)

#### Description:
Flask project that allows users to search for animes they have watched or view the latest/most popular animes. This is achieved using the Jikan API, which accesses data from MyAnimeList. Users can add and track animes they've previously watched and remove any added incorrectly. Multiple users can access their own individual anime lists via their accounts.

##### app.py:
The main file where the command "flask run" is used to start the website. It handles the overall logic and controls navigation between pages. Some functions are imported from other files as modules.  
E.g. `createUser()` is defined in `databasefunc.py` and used here by importing `databasefunc`.

These are the following routes:
 - `index()` - Returns `index.html`. Parameters `latest_animes` and `top_animes` are lists of anime objects representing the latest and most popular animes for the template to display.
 - `login()` - When the login button is pressed, checks if the user is already logged in. If so, redirects to their anime list. If not, it prompts for username/password and displays an error if incorrect.
 - `register()` - When the register button is pressed, checks if the username already exists. If it does, an error is shown; otherwise, it adds the new user to the database.
 - `logout()` - Clears the session and redirects to the index page.
 - `search()` - Accepts a POST request with a search query, uses the Jikan API to fetch results, and sends them to the template.
 - `add()` - Adds the selected anime to the user's anime list in the database and redirects to the list page.
 - `remove()` - Removes the selected anime from the user's list in the database and redirects to the list page.

##### database.db:
The SQLite database for the website. It stores all data on users, animes, and user-anime relationships for quick access.

Schema:
 - users - Stores: id, username, password
 - animes - Stores: anime id, name, image URL
 - animelists - Stores the `anime_id` and `user_id` combinations. Each row represents a specific anime added by a specific user.
   Example:
   (1, 4, 80), (2, 4, 100), (3, 5, 20), (4, 5, 40)
   => User 4 added animes 80 and 100, User 5 added 20 and 40.

##### databasefunc.py:
Contains all functions that access and manipulate the database using SQLite.

 - `createAnimeWithDataBaseId()` - Creates an anime object using the database ID. Faster than calling the API.
 - `getAnimesForUserId()` - Fetches animes from the database for a given user ID.
 - `insertAnime()` - Adds an anime to the user’s anime list.
 - `deleteAnime()` - Removes an anime from the user’s list.
 - `loginValid()` - Verifies the username/password combination against the database.
 - `getUserId()` - Retrieves a user's ID based on their username.
 - `userExists()` - Checks whether a username already exists in the database.
 - `createUser()` - Adds a new user to the database.
 - `getUsername()` - Retrieves a username given a user ID.

##### jikan.py:
Contains all functions that access the Jikan API.

Includes a class:
 - `Anime` - Stores the anime’s name, ID, and image URL. Has getter methods:
   - `getId()`
   - `getName()`
   - `getImage()`

Functions:
 - `getAnimeName()` - Retrieves the anime’s name from API data.
 - `getAnimeImage()` - Retrieves the image URL from API data.
 - `getAnimeId()` - Retrieves the anime ID from API data.
 - `createAnime()` - Combines the above functions to create an `Anime` object.
 - `searchAnimes()` - Sends a search query to the API and returns a list of `Anime` objects.
 - `getTopAnimes()`, `getLatestAnimes()` - Fetches top or latest animes from the API and returns them as `Anime` object lists.
