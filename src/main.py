import os
from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
from structlog import get_logger
from uuid import uuid4
from werkzeug.utils import secure_filename
from pathlib import Path
import json
import plotly
from PIL import Image ## Delete in production

from tasks.task_image_analysis import get_image_score, color_analysis, create_pie_fig
from tasks.task_connect_api import getSpotifyToken, getGenreSeeds, getRecommendations, getSeedFromGenre
from webapp.forms import ConfigForm, OutputForm

csrf = CSRFProtect()
log = get_logger(__name__)
app = Flask(__name__)
app.config["SECRET_KEY"] = uuid4().bytes
csrf.init_app(app)

@app.route("/genres", methods=["GET"])
def genres():
    bearer_token = getSpotifyToken()
    genre_list = getGenreSeeds(bearer_token)
    if (request.method == "GET"):
        return jsonify({"spotifyGenres": genre_list})

@csrf.exempt
@app.route("/analysis", methods=["GET", "POST"])
def analysis():
    if request.method == "POST":
        # Analysis variable prep
        bearer_token = getSpotifyToken()
        query_results_limit = 4
        target_genre = request.form['targetGenre']
        target_image = request.files['targetImage']
        # Analysis
        energy, loudness, tempo = get_image_score(target_image, reduc_factor=10)
        artist_seed, artist_seed_name = getSeedFromGenre(bearer_token, target_genre, 'artist', 50)
        track_seed, track_seed_name = getSeedFromGenre(bearer_token, target_genre, 'track', 50)
        recommendations = getRecommendations(bearer_token, query_results_limit, "US", artist_seed, target_genre, track_seed, energy, loudness, tempo)
        results = {
            "analyzed": True,
            "targetGenre": target_genre,
            "targetArtist": {
                "seed": artist_seed,
                "name": artist_seed_name
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
            } for i, rec in enumerate(recommendations["tracks"])]
        }
        return jsonify(results)
    elif request.method == "GET":
        return jsonify({"test": "hello"})

if __name__ == "__main__":
    # TODO: remove debug when in production
    app.run(debug=True)



