from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import base64
import os
from uuid import uuid4
from extract import extract_data

UPLOAD_FOLDER = 'flask/static/uploads'

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
            print(filename)
            return {'status': 'success', 'photo': filename}
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/photo', methods=['GET'])
def photo():
    if request.method == 'GET' and request.args.get('p') not in ['', None, 'undefined']:
        photo = os.path.join('/static/uploads/', request.args.get('p'))
        print(photo)
        return render_template('photo.html', photo=photo)
    else:
        return "Photo not found"


@app.route('/extract', methods=['GET'])
def extract():
    if request.method == 'GET' and request.args.get('p') not in ['', None, 'undefined']:
        photo = os.path.join(
            app.config['UPLOAD_FOLDER'], request.args.get('p'))
        grid = extract_data(photo)
        return render_template('extract.html', grid=grid, photo=photo.strip('flask'))
    else:
        return "Photo not found"


if __name__ == '__main__':
    app.run()
