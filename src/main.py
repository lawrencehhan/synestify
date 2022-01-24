import os
import urllib.request

from flask import Flask, render_template, redirect, url_for, request, session
from flask_wtf.csrf import CSRFProtect
from tempfile import TemporaryDirectory
from structlog import get_logger
from uuid import uuid4
from werkzeug.utils import secure_filename

from tasks.task_image_analysis import get_2d_image
from tasks.task_connect_api import getSpotifyToken, getRecommendations
from webapp.forms import ConfigForm, OutputForm

csrf = CSRFProtect()
log = get_logger(__name__)
app = Flask(__name__)
app.config['SECRET_KEY'] = uuid4().bytes
csrf.init_app(app)

@app.route('/', methods = ['POST', 'GET'])
def index():
    form = ConfigForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            
            # Process uploaded image and return calculated values
            uploaded_image_data = form.files.data
            uploaded_image_name = secure_filename(uploaded_image_data.filename)
            with TemporaryDirectory() as tmp_dir:
                try:
                    uploaded_image_saved_path = os.path.join(tmp_dir, uploaded_image_name)
                    uploaded_image_data.save(uploaded_image_saved_path)
                    log.info('Saved to: ' + uploaded_image_saved_path)
                    log.info('Converting image to 2d array: ')
                    outputImage = get_2d_image(uploaded_image_saved_path)
                    log.info(outputImage)
                except Exception as e:
                    log.error('Could not save image', error=e)
            
            # TODO: Configure recommendation inputs
            session['genre'] = form.genres.data
            log.info('Chosen genre: ' + session['genre'])
            return redirect(url_for('output'))
    return render_template('index.html', form=form)

@app.route('/output')
def output():

    form = OutputForm()
    chosen_genre = session['genre']
    chosen_artist = ''
    chosen_track = ''
    bearer_token = getSpotifyToken()
    recommendations = getRecommendations(bearer_token, 3, 'US', chosen_artist, chosen_genre, chosen_track)
    log.info(recommendations)

    recommendation_one_album_image_url, recommendation_one_name, recommendation_one_artist, recommendation_one_url = _get_recommendation_data_by_number(recommendations, 0)
    recommendation_two_album_image_url, recommendation_two_name, recommendation_two_artist, recommendation_two_url = _get_recommendation_data_by_number(recommendations, 1)
    recommendation_three_album_image_url, recommendation_three_name, recommendation_three_artist, recommendation_three_url = _get_recommendation_data_by_number(recommendations, 2)
    
    form.recommendation_one_album_image_url = recommendation_one_album_image_url
    form.recommendation_one_name.data = recommendation_one_name
    form.recommendation_one_artist.data = recommendation_one_artist
    form.recommendation_one_url.data = recommendation_one_url
    form.recommendation_two_album_image_url = recommendation_two_album_image_url
    form.recommendation_two_name.data = recommendation_two_name
    form.recommendation_two_artist.data = recommendation_two_artist
    form.recommendation_two_url.data = recommendation_two_url
    form.recommendation_three_album_image_url = recommendation_three_album_image_url
    form.recommendation_three_name.data = recommendation_three_name
    form.recommendation_three_artist.data = recommendation_three_artist
    form.recommendation_three_url.data = recommendation_three_url
    return render_template('output.html', form=form)


def _get_recommendation_data_by_number(recommendations: dict, recommendation_number: int):
    recommendation_album_image_url = recommendations["tracks"][recommendation_number]["album"]["images"][0]["url"]
    recommendation_name = recommendations["tracks"][recommendation_number]["name"]
    recommendation_artist = recommendations["tracks"][recommendation_number]["artists"][0]["name"]
    recommendation_url = recommendations["tracks"][recommendation_number]["external_urls"]["spotify"]
    return recommendation_album_image_url, recommendation_name, recommendation_artist, recommendation_url

if __name__ == '__main__':
    #TODO: remove debug when in production
	app.run(debug=True)
