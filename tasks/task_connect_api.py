import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

os.environ["SPOTIPY_CLIENT_ID"] = "094f39d25a5d45c3b0671baa71d58425"
os.environ["SPOTIPY_CLIENT_SECRET"] = "bbd8a243877d4092ba5774484b41dc2e"

def getTracks(query: str):
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ['SPOTIPY_CLIENT_ID'],
                                                            client_secret=os.environ['SPOTIPY_CLIENT_SECRET']))

    results = sp.search(q=query, limit=20)   
    for idx, track in enumerate(results['tracks']['items']):
        print(idx, track['name'])
    return results

def sampleFunction(input):
    output = input + 2
    return output

getTracks('drake')