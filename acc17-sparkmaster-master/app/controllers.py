from app import app
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from heplers import verify_token
from werkzeug import secure_filename
import json

import os

import glob

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'

app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'csv'])

@app.route("/jupyter/token", methods=['POST'])
def get_jupyter_token():
    token = request.headers['Authorization']
    response_data = {}
    if verify_token(token) is None:
        response_data['verify_token'] = False
    else:
        response_data['verify_token'] = True

        try:
            filename = glob.glob("/home/ubuntu/.local/share/jupyter/runtime/*.json")[0]
            with open(filename, "r") as f:
                data = json.loads(f.read())
            response_data['success'] = True
            response_data['port'] = data['port']
            response_data['token'] = data['token']
        except IndexError:
            response_data['success'] = False
            response_data['message'] = 'Cannot find jupyter token'

    return json.dumps(response_data)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload')
def index():
    return render_template('index.html')

@app.route('/uploaded', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filenames.append(filename)
    return render_template('upload.html', filenames=filenames)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
