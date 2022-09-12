from flask import Flask, jsonify, request, Response
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from structlog import get_logger
from uuid import uuid4

from task_image_analysis import get_image_score
from task_connect_api import getSpotifyToken, getGenreSeeds, getRecommendations, getArtistSeedFromGenre, getTrackSeedFromArtist

csrf = CSRFProtect()
log = get_logger(__name__)
application = Flask(__name__)
application.config["SECRET_KEY"] = uuid4().bytes
csrf.init_app(application)
cors_resources = {
    r"/*": {
        "origins": [
            "https://www.synestify.com",
            "http://synestify.com.s3-website-us-west-1.amazonaws.com"
            ]
    }
}
CORS(application, resources=cors_resources)

@application.route("/")
def starting_url():
	status_code = Response(status=200)
	return status_code

@application.route("/status", methods=["GET"])
def status():
    if (request.method == "GET"):
        return jsonify({"status": "online"})

@application.route("/genres", methods=["GET"])
def genres():
    bearer_token = getSpotifyToken()
    genre_list = getGenreSeeds(bearer_token)
    if (request.method == "GET"):
        return jsonify({"spotifyGenres": genre_list})

@csrf.exempt
@application.route("/analysis", methods=["GET", "POST"])
def analysis():
    if request.method == "POST":
        # Analysis variable prep
        bearer_token = getSpotifyToken()
        query_results_limit = 12
        target_genre = request.form['targetGenre']
        # log.info(f'Target genre: {target_genre}')
        target_image = request.files['targetImage']
        # log.info(f'Target image: {target_image.name}')

        # Analysis
        energy, loudness, tempo = get_image_score(target_image, reduc_factor=10)
        _, artist_seed_name_popular, artist_seed_second, artist_seed_name_second = getArtistSeedFromGenre(bearer_token, target_genre, 50)
        track_seed, track_seed_name = getTrackSeedFromArtist(bearer_token, artist_seed_name_popular, 50)
        recommendations = getRecommendations(bearer_token, query_results_limit, "US", artist_seed_second, target_genre, track_seed, energy, loudness, tempo)
        # df = color_analysis(target_image)
        # pie_fig = create_pie_fig(df)
        # graphJSON = json.dumps(pie_fig, cls=plotly.utils.PlotlyJSONEncoder)
        # graphJSON = pie_fig.to_json()
        results = {
            "analyzed": True,
            "targetGenre": target_genre,
            "targetArtist": {
                "seed": artist_seed_second,
                "name": artist_seed_name_second
            },
            "targetTrack": {
                "seed": track_seed,
                "name": track_seed_name
            },
            "score": {
                "energy": energy,
                "loudness": loudness,
                "tempo": tempo
            },
            "recommendations": [{
                    "trackID": i,
                    "albumCover": rec["album"]["images"][0]["url"],
                    "trackName": rec["name"],
                    "artist": rec["artists"][0]["name"],
                    "url": rec["external_urls"]["spotify"]
                } for i, rec in enumerate(recommendations["tracks"])
            ]
        }
        # log.info(jsonify(results))
        return jsonify(results)
    elif request.method == "GET":
        return jsonify({"test": "hello"})

if __name__ == "__main__":
    application.run(debug=True)



