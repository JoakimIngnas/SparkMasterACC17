# app/helpers.py

import jwt
import app
from run import app

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    except:
        return None
    return payload['user_id']
    # Signature has expired
