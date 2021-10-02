from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired, FileAllowed

class ConfigForm(FlaskForm):
    files = FileField(label="Upload Image", validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png'], 'Image files only!')])
    submit = SubmitField(label="Submit")
