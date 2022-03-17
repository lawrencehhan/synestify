from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from tasks.task_connect_api import getSpotifyToken, getGenreSeeds

bearer_token = getSpotifyToken()
genre_list = getGenreSeeds(bearer_token)


class ConfigForm(FlaskForm):
    files = FileField(
        label="Upload Image",
        validators=[
            FileRequired(),
            FileAllowed(["jpg", "jpeg", "png"], "Image files only!"),
        ],
    )
    genres = SelectField(
        label="Choose Favorite Genre", choices=[genre for genre in genre_list]
    )
    artist = StringField(
        label="Enter Favorite Artist (Full Artist Name)", validators=[DataRequired()]
    )
    track = StringField(
        label="Enter Favorite Track (Full Track Name)", validators=[DataRequired()]
    )
    submit = SubmitField(label="Synestify")


class OutputForm(FlaskForm):
    recommendation_one_album_image_url = ""
    recommendation_one_name = TextAreaField(label="Track Name")
    recommendation_one_artist = TextAreaField(label="Artist Name")
    recommendation_one_url = TextAreaField(label="Track URL")

    recommendation_two_album_image_url = ""
    recommendation_two_name = TextAreaField(label="Track Name")
    recommendation_two_artist = TextAreaField(label="Artist Name")
    recommendation_two_url = TextAreaField(label="Track URL")

    recommendation_three_album_image_url = ""
    recommendation_three_name = TextAreaField(label="Track Name")
    recommendation_three_artist = TextAreaField(label="Artist Name")
    recommendation_three_url = TextAreaField(label="Track URL")
