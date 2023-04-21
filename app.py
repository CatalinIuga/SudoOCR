import base64
import json
import os
from uuid import uuid4

from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from extract import extract_data

UPLOAD_FOLDER = 'static/uploads'

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        photo = request.form['photo_data']
        if photo not in ['', None, 'undefined']:
            photo = photo.split(',')[1]
            photo = base64.b64decode(photo)
            filename = secure_filename(uuid4().hex + '.png')
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'wb') as f:
                f.write(photo)
            return {'status': 'success', 'photo': filename}
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

# return the photo


@app.route('/photo', methods=['GET'])
def photo():
    if request.method == 'GET' and request.args.get('p') not in ['', None, 'undefined']:
        photo = os.path.join('/static/uploads/', request.args.get('p'))
        print(photo)
        return render_template('photo.html', photo=photo)
    else:
        return "Photo not found"

# extract the data from the photo and return the grid


@app.route('/extract', methods=['GET'])
def extract():
    if request.method == 'GET' and request.args.get('p') not in ['', None, 'undefined']:
        photo = os.path.join(
            app.config['UPLOAD_FOLDER'], request.args.get('p'))
        try:
            grid = extract_data(photo)
        except Exception as e:
            print(e)
            return render_template('extract.html', grid=None, photo=photo, error="No photo found")
        return render_template('extract.html', grid=grid, photo=photo, error=None)
    else:
        return "Photo not found"


if __name__ == '__main__':
    app.run()
