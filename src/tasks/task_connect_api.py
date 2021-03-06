import base64
from dotenv import load_dotenv
import json
import os
import requests
from structlog import get_logger
from random import randint


load_dotenv()


log = get_logger(__name__)
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def getSpotifyToken():
    # Client Credentials Flow: https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
    authUrl = "https://accounts.spotify.com/api/token"

    message = f"{CLIENT_ID}:{CLIENT_SECRET}".encode("ascii")
    base64_message = base64.b64encode(message).decode("ascii")

    auth_headers = {"Authorization": "Basic " + base64_message}
    auth_data = {"grant_type": "client_credentials"}
    response = requests.post(authUrl, data=auth_data, headers=auth_headers)
    try:
        bearer_token = (json.loads(response.content.decode("ascii")))["access_token"]
    except:
        log.error("Invalid Client ID or Client Secret in .env file")
        quit()
    return bearer_token


def getGenreSeeds(bearer_token: str):
    # Get list of genres: https://developer.spotify.com/console/get-available-genre-seeds/
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    genre_list = sendGetRequest(bearer_token, url)
    return genre_list["genres"]


def getSearchResults(bearer_token: str, query: str, search_type: str, limit: int):
    # Get recommended songs: https://developer.spotify.com/console/get-recommendations/
    url = _createSearchUrl(query, search_type, limit)
    search_results = sendGetRequest(bearer_token, url)
    return search_results


def getRecommendations(
    bearer_token: str,
    limit: int,
    market: str,
    seed_artists: str,
    seed_genres: str,
    seed_tracks: str,
    target_energy: float,
    target_loudness: float,
    target_tempo: float
):
    # Get recommended songs: https://developer.spotify.com/console/get-recommendations/
    url = _createRecommendationsUrl(
        limit, market, seed_artists, seed_genres, seed_tracks, target_energy, target_loudness, target_tempo
    )
    recommendations = sendGetRequest(bearer_token, url)
    return recommendations


def sendGetRequest(bearer_token: str, url: str):
    headers = {"Authorization": "Bearer " + bearer_token}
    response = requests.get(url, headers=headers)
    response_content = response.json()
    return response_content


def _createSearchUrl(query: str, search_type: str, limit: int):
    base_url = "https://api.spotify.com/v1/search?"
    query = "q=" + query.replace(" ", "%20")
    search_type = "&type=" + search_type
    limit = "&limit=" + str(limit)
    search_url = base_url + query + search_type + limit
    return search_url


def _createRecommendationsUrl(
    limit: int, 
    market: str, 
    seed_artist: str, 
    seed_genre: str, 
    seed_track: str,
    target_energy: float,
    target_loudness: float,
    target_tempo: float
):
    base_url = "https://api.spotify.com/v1/recommendations?"
    limit = "limit=" + str(limit)
    market = "&market=US"
    seed_artist = (
        "&seed_artists=" + seed_artist
    )  # Example: 3TVXtAsR1Inumwj472S9r4 Drake
    seed_genre = "&seed_genres=" + seed_genre  # Example: pop
    seed_track = (
        "&seed_tracks=" + seed_track
    )  # Example: 7wcWkzT1X75DguAwOWxlGt Way 2 Sexy
    target_energy = "&target_energy=" + str(target_energy)
    target_loudness = "&target_loudness=" + str(target_loudness)
    target_tempo = "&target_tempo=" + str(target_tempo)

    recommendations_url = (
        base_url + limit + market + seed_artist + seed_genre + seed_track + target_energy + target_loudness + target_tempo
    )
    return recommendations_url


def getSeedFromGenre(bearer_token: str, seed_genre: str, search_type: str, total_seeds: int):
    seeds = getSearchResults(bearer_token, f"genre:{seed_genre}", search_type, total_seeds)
    seed_selection = randint(0, total_seeds-1)
    seed = seeds[f'{search_type}s']['items'][seed_selection]
    seed_id = seed['id']
    seed_name = seed['name']
    return (seed_id, seed_name)


### No longer needed
def getCategories(bearer_token: str):
    categories_url = "https://api.spotify.com/v1/browse/categories?limit=50" # limit is capped at 50
    categories_json = sendGetRequest(bearer_token, categories_url)
    categories_list = categories_json['categories']['items']
    categories_list = [item['id'] for item in categories_list]
    return categories_list
    

def getGenreCategoriesOverlap(bearer_token: str):
    categories_url = 'https://api.spotify.com/v1/browse/categories?limit=50' # limit is capped at 50
    categories_json = sendGetRequest(bearer_token, categories_url)
    categories_list = categories_json['categories']['items']
    categories_list = [category for item in categories_list for category in item['id'].split('_')]
    
    genre_list = getGenreSeeds(bearer_token)
    genre_list = [genre.replace('-', '') for genre in genre_list]

    overlap_list = [genre for genre in genre_list if (genre in categories_list)]
    return overlap_list

# make two dictionaries referencing back each change to the original respective names so
# 1) can access category for artist and song rec
# 2) can access genre seed
