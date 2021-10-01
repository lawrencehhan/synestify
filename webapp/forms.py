from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField

class ConfigForm(FlaskForm):
    files = FileField(label="Upload Image")
    submit = SubmitField(label="Proceed")