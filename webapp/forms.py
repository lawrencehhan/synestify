from wtforms import Form, FileField, SubmitField

class ConfigForm(Form):
    files = FileField(label="Upload Image")
    submit = SubmitField(label="Submit")