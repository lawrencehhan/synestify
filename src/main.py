import os

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf.csrf import CSRFProtect
from tempfile import TemporaryDirectory
from structlog import get_logger
from uuid import uuid4
from werkzeug.utils import secure_filename

from tasks.task_image_analysis import get_2d_image
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
            log.info('Clicked on submit')
            file_data = form.files.data
            file_name = secure_filename(file_data.filename)
            with TemporaryDirectory() as tmp_dir:
                log.info('Begin saving uploaded file')
                try:
                    file_saved_path = os.path.join(tmp_dir, file_name)
                    file_data.save(file_saved_path)
                    log.info('Saved to: ' + file_saved_path)
                    log.info('Converting image to 2d array: ')
                    outputImage = get_2d_image(file_saved_path)
                    log.info(outputImage)
                except Exception as e:
                    log.error('Could not save image', error=e)
            return redirect(url_for('output'))
    return render_template('index.html', form=form)

@app.route('/output')
def output():
    return render_template('output.html')







if __name__ == '__main__':
    #TODO: remove debug when in production
	app.run(debug=True)
