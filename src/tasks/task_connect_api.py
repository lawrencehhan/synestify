import base64
import json
import requests

client_id = "094f39d25a5d45c3b0671baa71d58425"
client_secret = "bbd8a243877d4092ba5774484b41dc2e"

def getRecommendations():
    bearer_token = getSpotifyToken()['access_token']
    url = createRecommendationsUrl()
    headers = {"Authorization": "Bearer " + bearer_token}
    response = requests.get(url, headers=headers)
    recommendations = json.loads(response.content.decode("ascii"))
    return recommendations

def getSpotifyToken():
    authUrl = 'https://accounts.spotify.com/api/token'

    message = f"{client_id}:{client_secret}".encode("ascii")
    base64_message = base64.b64encode(message).decode("ascii")

    auth_headers = {"Authorization": "Basic " + base64_message}
    auth_data = {"grant_type": "client_credentials"}
    response = requests.post(authUrl, data=auth_data, headers=auth_headers)
    bearer_token = json.loads(response.content.decode("ascii"))
    return bearer_token
    
def createRecommendationsUrl():
    base_url = "https://api.spotify.com/v1/recommendations?"
    limit = "limit=3"
    market = "&market=US"
    seed_artists = "&seed_artists=3TVXtAsR1Inumwj472S9r4"
    seed_genres = "&seed_genres=pop"
    seed_tracks = "&seed_tracks=7wcWkzT1X75DguAwOWxlGt"
    recommendations_url = base_url + limit + market + seed_artists + seed_genres + seed_tracks
    return recommendations_url


# def getArtistIds(): 
    # search for artist seed ids
    # GET https://api.spotify.com/v1/search
