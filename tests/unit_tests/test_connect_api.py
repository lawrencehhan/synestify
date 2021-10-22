from src.tasks.task_connect_api import getSpotifyToken, getRecommendations, getGenreSeeds

class TestAPIConnection():

    def test_get_spotify_token(self):
        spotify_token = getSpotifyToken()
        assert spotify_token != None

    def test_get_recommendations(self):
        bearer_token = getSpotifyToken()
        limit = "limit=3"
        market = "&market=US"
        seed_artists = "&seed_artists=3TVXtAsR1Inumwj472S9r4" # Artist: Drake
        seed_genres = "pop"
        seed_tracks = "&seed_tracks=1zi7xx7UVEFkmKfv06H8x0?si=d9e66edcdd9648bf" # Song: One Dance
        response = getRecommendations(bearer_token, limit, market, seed_artists, seed_genres, seed_tracks)
        a = 1
    
    def test_get_genre_seeds(self):
        bearer_token = getSpotifyToken()
        genre_seed_list = getGenreSeeds(bearer_token)
        print('1')

