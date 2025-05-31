import base64
from flask import jsonify,json,make_response,flash
from werkzeug.exceptions import Conflict, BadRequest
from Crypto.Cipher import AES
from datetime import datetime, timedelta
from Crypto.Hash import SHA256
import jwt
import os
from time import time

PAD = "X"

def key_hash(key):
    return SHA256.new(key.encode()).digest()

def encrypt(text, key):
    while len(text) % 32 != 0:
        text += PAD
    cipher = AES.new(key_hash(key))
    encrypted = cipher.encrypt(text.encode())
    return base64.b64encode(encrypted).decode()

def decrypt(text, key):
    cipher = AES.new(key_hash(key))
    plain = cipher.decrypt(base64.b64decode(text))
    return plain.decode().rstrip(PAD)

def sendResponse(message,data=None):
    obj=jsonify({"message":message,"status":200,"data":data})
    return make_response(obj, 200)

def sendResponseByStatus(message,status):
    obj=jsonify({"message":message,"status":status})
    return make_response(obj, status)

def handle_bad_request(e):
    data =jsonify({"message":e.args[0] })
    return make_response(data, 400)

def getMessage(message):
    try:
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "locales", "messages.json")
        data = json.load(open(json_url))
        return data[message]
    except Exception as e:
        return handle_bad_request(e)
    

def getJSONData(path):
    try:
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        json_url = os.path.join(SITE_ROOT, "locales", path+".json")
        data = json.load(open(json_url))
        return data
    except Exception as e:
        return handle_bad_request(e)
    

def set_cookie_value(obj,status,name,value):
    res= make_response(obj, status)
    res.set_cookie(name, value)
    return res
    
def get_cookie_value(req,name):
    return req.cookies.get(name)

def generateToken(string):
    try:
        token = jwt.encode({'public_id': string,'exp' : datetime.utcnow() + timedelta(minutes = 30)},os.getenv('TOKEN_SECRET_KEY'))
        return token
    except Exception as e:
        return handle_bad_request(e)
    
def verifyToken(token):
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded
    except Exception as e:
        return False


def get_time_stamp():
    milliseconds = int(time() * 1000)
    return milliseconds

def get_extension(filename):
     return filename.rsplit('.', 1)[1].lower()



