import os

from flask import Flask, render_template, redirect, url_for, request
from tempfile import TemporaryDirectory
from structlog import get_logger

from forms import ConfigForm

log = get_logger(__name__)
app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def index():
    form = ConfigForm()
    file_data = form.files.data

    if request.method == 'POST':
        # with TemporaryDirectory() as tmp_dir:
        #     file_data.save(os.path.join(tmp_dir, file_data.filename))
        return redirect(url_for('output'))
    return render_template('index.html', form=form)

@app.route('/output')
def output():
    return render_template('output.html')







if __name__ == '__main__':
    #TODO: remove debug when in production
	app.run(debug=True)
