from flask import Flask, render_template
from tempfile import TemporaryDirectory
from structlog import get_logger

from webapp.forms import ConfigForm

log = get_logger(__name__)
app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    form = ConfigForm()
    file_data = form.files.data

    # if form.validate_on_submit():
    return render_template('index.html')








if __name__ == '__main__':
    #TODO: remove debug when in production
	app.run(debug=True)
