import os
from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
from structlog import get_logger
from uuid import uuid4
from werkzeug.utils import secure_filename
from pathlib import Path
import json
import plotly

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


@app.route("/analysis", methods=["POST", "GET"])
def analysis():
    if request.method == "POST":
        target_genre = request.json['targetGenre']
        return target_genre

@app.route("/", methods=["POST", "GET"])
def index():
    form = ConfigForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Process uploaded image and return calculated values
            uploaded_image_data = form.files.data
            uploaded_image_name = secure_filename(uploaded_image_data.filename)
            session["image_name"] = uploaded_image_name

            uploaded_image_save_path = os.path.join(Path(__file__).parent, 'static', 'assets', 'submissions', uploaded_image_name)
            uploaded_image_data.save(uploaded_image_save_path)
            log.info(f"Image saved to: {uploaded_image_save_path}")

            energy, loudness, tempo = get_image_score(uploaded_image_save_path, 10)
            session["energy"], session["loudness"], session["tempo"] = energy, loudness, tempo
            log.info(f'Image scores (energy, loudness, tempo) found to be: {energy}, {loudness}, {tempo}')

            session["user_genre"] = form.genres.data
            return redirect(url_for("output"))
    return render_template("index.html", form=form)


@app.route("/output")
def output():
    form = OutputForm()
    bearer_token = getSpotifyToken()
    query_results_limit = 3
    log.info("User submitted image: " + session["image_name"])

    user_genre = session["user_genre"]
    log.info("User chosen genre: " + session["user_genre"])
    user_artist_seed, user_artist_name = getSeedFromGenre(bearer_token, user_genre, 'artist', 50)
    log.info("User generated artist: " + user_artist_name)
    user_track_seed, user_track_name = getSeedFromGenre(bearer_token, user_genre, 'track', 50)
    log.info("User generated track: " + user_track_name)
    analysis_targets = (session["energy"], session["loudness"], session["tempo"])
    target_energy, target_loudness, target_tempo = analysis_targets
    log.info(f"Analyzed targets (energy, loudness, tempo): {target_energy}, {target_loudness}, {target_tempo}")

    recommendations = getRecommendations(bearer_token, query_results_limit, "US", user_artist_seed, user_genre, user_track_seed, target_energy, target_loudness, target_tempo)
    form.recommendation_one_album_image_url, form.recommendation_one_name.data, form.recommendation_one_artist.data, form.recommendation_one_url.data = _get_recommendation_data_by_number(recommendations, 0)
    form.recommendation_two_album_image_url, form.recommendation_two_name.data, form.recommendation_two_artist.data, form.recommendation_two_url.data = _get_recommendation_data_by_number(recommendations, 1)
    form.recommendation_three_album_image_url, form.recommendation_three_name.data, form.recommendation_three_artist.data, form.recommendation_three_url.data = _get_recommendation_data_by_number(recommendations, 2)
    log.info("Recommendation 1: " + form.recommendation_one_name.data + " by " + form.recommendation_one_artist.data)
    log.info("Recommendation 2: " + form.recommendation_two_name.data + " by " + form.recommendation_two_artist.data)
    log.info("Recommendation 3: " + form.recommendation_three_name.data + " by " + form.recommendation_three_artist.data)
    
    img_path = os.path.join(Path(__file__).parent, 'static', 'assets', 'submissions', session["image_name"])
    df = color_analysis(img_path)
    pie_fig = create_pie_fig(df)
    graphJSON = json.dumps(pie_fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("output.html", form=form, image_name=session["image_name"], analysis_targets=analysis_targets, graphJSON=graphJSON)


def _get_recommendation_data_by_number(
    recommendations: dict, recommendation_number: int
):
    recommendation_album_image_url = recommendations["tracks"][recommendation_number]["album"]["images"][0]["url"]
    recommendation_name = recommendations["tracks"][recommendation_number]["name"]
    recommendation_artist = recommendations["tracks"][recommendation_number]["artists"][0]["name"]
    recommendation_url = recommendations["tracks"][recommendation_number]["external_urls"]["spotify"]
    return recommendation_album_image_url, recommendation_name, recommendation_artist, recommendation_url

if __name__ == "__main__":
    # TODO: remove debug when in production
    app.run(debug=True)
