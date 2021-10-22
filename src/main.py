import os

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf.csrf import CSRFProtect
from tempfile import TemporaryDirectory
from structlog import get_logger
from uuid import uuid4
from werkzeug.utils import secure_filename

from tasks.task_image_analysis import get_2d_image
from tasks.task_connect_api import getSpotifyToken, getRecommendations
from webapp.forms import ConfigForm

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
            
            # Configure recommendation inputs
            chosen_genre = form.genres.data
            log.info('Chosen genre: ' + chosen_genre)
            chosen_artist = ''
            chosen_track = ''
            bearer_token = getSpotifyToken()
            recommendations = getRecommendations(bearer_token, 3, 'US', chosen_artist, chosen_genre, chosen_track)
            log.info(recommendations)
            return redirect(url_for('output'))
    return render_template('index.html', form=form)

@app.route('/output')
def output():
    return render_template('output.html')







if __name__ == '__main__':
    #TODO: remove debug when in production
	app.run(debug=True)
