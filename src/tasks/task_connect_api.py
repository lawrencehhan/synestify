import base64
import json
import requests

# Nonsensitive credentials
client_id = "094f39d25a5d45c3b0671baa71d58425"
client_secret = "bbd8a243877d4092ba5774484b41dc2e"

def getSpotifyToken():
    # Client Credentials Flow: https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
    authUrl = 'https://accounts.spotify.com/api/token'

    message = f"{client_id}:{client_secret}".encode("ascii")
    base64_message = base64.b64encode(message).decode("ascii")

    auth_headers = {"Authorization": "Basic " + base64_message}
    auth_data = {"grant_type": "client_credentials"}
    response = requests.post(authUrl, data=auth_data, headers=auth_headers)
    bearer_token = (json.loads(response.content.decode("ascii")))['access_token']
    return bearer_token

def sendGetRequest(bearer_token, url):
    headers = {"Authorization": "Bearer " + bearer_token}
    response = requests.get(url, headers=headers)
    response_content = response.json()
    return response_content

def createRecommendationsUrl(limit, market, seed_artists, seed_genres, seed_tracks):
    base_url = "https://api.spotify.com/v1/recommendations?"
    limit = "limit=3"
    market = "&market=US"
    seed_artists = "&seed_artists=3TVXtAsR1Inumwj472S9r4" # Drake
    seed_genres = "&seed_genres=" + seed_genres
    seed_tracks = "&seed_tracks=7wcWkzT1X75DguAwOWxlGt" # Way 2 Sexy
    recommendations_url = base_url + limit + market + seed_artists + seed_genres + seed_tracks
    return recommendations_url

def getRecommendations(bearer_token, limit, market, seed_artists, seed_genres, seed_tracks):
    # Get recommended songs: https://developer.spotify.com/console/get-recommendations/
    url = createRecommendationsUrl(limit, market, seed_artists, seed_genres, seed_tracks)
    recommendations = sendGetRequest(bearer_token, url)
    return recommendations

def getArtistIds(): 
    # Search for artist seed ids https://api.spotify.com/v1/search
    return 

def getGenreSeeds(bearer_token):
    # Get list of genres: https://developer.spotify.com/console/get-available-genre-seeds/
    url = "	https://api.spotify.com/v1/recommendations/available-genre-seeds"
    genre_list = sendGetRequest(bearer_token, url)
    return genre_list['genres']
