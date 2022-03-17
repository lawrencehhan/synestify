import os

from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf.csrf import CSRFProtect
from tempfile import TemporaryDirectory
from structlog import get_logger
from uuid import uuid4
from werkzeug.utils import secure_filename

from tasks.task_image_analysis import get_image_score
from tasks.task_connect_api import getSpotifyToken, getRecommendations, getSearchResults
from webapp.forms import ConfigForm, OutputForm

csrf = CSRFProtect()
log = get_logger(__name__)
app = Flask(__name__)
app.config["SECRET_KEY"] = uuid4().bytes
csrf.init_app(app)


@app.route("/", methods=["POST", "GET"])
def index():
    form = ConfigForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Process uploaded image and return calculated values
            uploaded_image_data = form.files.data
            uploaded_image_name = secure_filename(uploaded_image_data.filename)
            with TemporaryDirectory() as tmp_dir:
                try:
                    uploaded_image_saved_path = os.path.join(
                        tmp_dir, uploaded_image_name
                    )
                    uploaded_image_data.save(uploaded_image_saved_path)
                    log.info("Image temporarily saved to: " + uploaded_image_saved_path)
                except Exception as e:
                    log.error("Could not save image", error=e)
            return redirect(url_for("main"))
    return render_template("index.html", form=form)


@app.route("/main", methods=["POST", "GET"])
def main():
    form = ConfigForm()
    if request.method == "POST":
        if form.validate_on_submit():
            # Save all musical parameters to session
            session["user_genre"] = form.genres.data
            session["user_artist"] = form.artist.data
            session["user_track"] = form.track.data
            return redirect(url_for("output"))
    return render_template("main.html", form=form)


@app.route("/output")
def output():

    form = OutputForm()
    bearer_token = getSpotifyToken()
    query_results_limit = 3

    artist_search_results = getSearchResults(bearer_token, session['user_artist'], "artist", query_results_limit)
    user_artist_seed = artist_search_results["artists"]["items"][0]["id"] if artist_search_results else "No artist seed found"
    log.info("Found favorite artist: " + artist_search_results["artists"]["items"][0]["name"])

    track_search_results = getSearchResults(bearer_token, session['user_track'], "track", query_results_limit)
    user_track_seed = track_search_results["tracks"]["items"][0]["id"] if track_search_results else "No track seed found"
    log.info("Found favorite track: " + track_search_results["tracks"]["items"][0]["name"] + " by " + track_search_results["tracks"]["items"][0]["artists"][0]["name"])

    user_genre = session["user_genre"]
    log.info("User chosen genre: " + session["user_genre"])

    recommendations = getRecommendations(bearer_token, query_results_limit, "US", user_artist_seed, user_genre, user_track_seed)
    form.recommendation_one_album_image_url, form.recommendation_one_name.data, form.recommendation_one_artist.data, form.recommendation_one_url.data = _get_recommendation_data_by_number(recommendations, 0)
    form.recommendation_two_album_image_url, form.recommendation_two_name.data, form.recommendation_two_artist.data, form.recommendation_two_url.data = _get_recommendation_data_by_number(recommendations, 1)
    form.recommendation_three_album_image_url, form.recommendation_three_name.data, form.recommendation_three_artist.data, form.recommendation_three_url.data = _get_recommendation_data_by_number(recommendations, 2)
    log.info("Recommendation 1: " + form.recommendation_one_name.data + " by " + form.recommendation_one_artist.data)
    log.info("Recommendation 2: " + form.recommendation_two_name.data + " by " + form.recommendation_two_artist.data)
    log.info("Recommendation 3: " + form.recommendation_three_name.data + " by " + form.recommendation_three_artist.data)
    return render_template("output.html", form=form)


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
