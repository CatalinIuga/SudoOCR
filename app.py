import base64
import json
import os
from uuid import uuid4

from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

from extract import extract_data
from solve import solve_sudoku

UPLOAD_FOLDER = 'static/uploads'
SOLUTION_FOLDER = 'static/solved'

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG'] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SOLUTION_FOLDER'] = SOLUTION_FOLDER


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
        try:
            grid = extract_data(photo)
        except Exception as e:
            print(e)
            return render_template('extract.html', grid=None, photo=None, error="No photo found")
        return render_template('extract.html', grid=grid, photo=photo, error=None)
    else:
        return "Photo not found"


@app.route('/solve', methods=['POST', 'GET'])
def solve():
    if request.method == 'POST' and request.form['table'] not in ['', None, 'undefined']:
        photo_id = ''

        if request.form['photo'] not in ['', None, 'undefined']:
            photo_id = request.form['photo'].split(
                '=')[1].strip('.png')+'.json'
        else:
            photo_id = uuid4().hex + '.json'
        print(photo_id)
        solution = os.path.join(
            app.config['SOLUTION_FOLDER'], photo_id)
        print(solution)
        table = json.loads(request.form['table'])
        solved = solve_sudoku(table)

        if solved:
            with open(solution, 'w') as f:
                final = {'solved': solved,
                         'photo': photo_id.strip('.json')}
                final = json.dumps(final)
                f.write(final)
            return {'status': 'success', 'id': photo_id}
        else:
            return {'status': 'error', 'message': 'No solution found'}
    elif request.method == 'GET' and request.args.get('p') not in ['', None, 'undefined']:
        data = os.path.join(
            app.config['SOLUTION_FOLDER'], request.args.get('p'))
        with open(data, 'r') as f:
            data = json.loads(f.read())
        return render_template('solved.html', solved=data['solved'])


if __name__ == '__main__':
    app.run()
