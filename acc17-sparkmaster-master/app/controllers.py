from app import app
from flask import request
from heplers import verify_token
import json

import glob

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