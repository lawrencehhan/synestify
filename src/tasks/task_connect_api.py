import base64
from dotenv import load_dotenv
import json
import os
import requests
from structlog import get_logger


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
    url = "	https://api.spotify.com/v1/recommendations/available-genre-seeds"
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
):
    # Get recommended songs: https://developer.spotify.com/console/get-recommendations/
    url = _createRecommendationsUrl(
        limit, market, seed_artists, seed_genres, seed_tracks
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
    limit: int, market: str, seed_artist: str, seed_genre: str, seed_track: str
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
    recommendations_url = (
        base_url + limit + market + seed_artist + seed_genre + seed_track
    )
    return recommendations_url
