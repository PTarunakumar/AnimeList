import requests
#All the functions in this file are used to interact with the Jikan API, where I got the anime data from

#Anime class to store anime data
class Anime:
    def __init__(self, id, name, image):
        self.id = id
        self.name = name
        self.image = image

    #Getters
    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getImage(self):
        return self.image

#Extracts anime name from data (dictionary on one anime) from Jikan API
def getAnimeName(data):
    return data['title']

#Extracts anime image url from data (dictionary on one anime) from Jikan API
def getAnimeImage(data):
    return data['images']['jpg']['large_image_url']

#Extracts anime id from data (dictionary on one anime) from Jikan API
def getAnimeId(data):
    return int(data['mal_id'])

#Extracts anime data from Jikan API based on anime id
def getAnime(id):
    return requests.get(f"https://api.jikan.moe/v4/anime/{id}", timeout=0.5).json()['data']

#Creates an anime object from Jikan API based on anime id
def createAnime(id):
    anime = getAnime(id)
    return Anime(id, getAnimeName(anime), getAnimeImage(anime))

#Searches for animes based on user input, returns a list of anime objects
def searchAnimes(name):
    output = []
    data = requests.get(f'https://api.jikan.moe/v4/anime?q={name}', timeout=0.5).json()['data']
    for anime in data:
        output.append(Anime(getAnimeId(anime), getAnimeName(anime), getAnimeImage(anime)))
    return output

#Searches for top x animes via Jikan API byPopularity filter, returns a list of anime objects
def getTopAnimes():
    output = []
    MAX_COUNT = 5
    data = requests.get(f"https://api.jikan.moe/v4/top/anime?filter=bypopularity&limit={MAX_COUNT}", timeout=0.5).json()['data'][:MAX_COUNT]
    for anime in data:
        output.append(Anime(getAnimeId(anime), getAnimeName(anime), getAnimeImage(anime)))
    return output


#Searches for latest x animes via Jikan API byAiring filter, returns a list of anime objects
def getLatestAnimes():
    output = []
    MAX_COUNT = 5
    data = requests.get(f"https://api.jikan.moe/v4/top/anime?filter=airing&limit={MAX_COUNT}", timeout=0.5).json()['data'][:MAX_COUNT]
    for anime in data:
        output.append(Anime(getAnimeId(anime), getAnimeName(anime), getAnimeImage(anime)))
    return output