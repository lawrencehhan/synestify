from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed

from tasks.task_connect_api import getSpotifyToken, getGenreSeeds

bearer_token = getSpotifyToken()
genre_list = getGenreSeeds(bearer_token)

class ConfigForm(FlaskForm):
    files = FileField(label="Upload Image", validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Image files only!')])
    genres = SelectField(label='Choose Favorite Genre', 
        choices=[genre for genre in genre_list])
    submit = SubmitField(label="Submit")
