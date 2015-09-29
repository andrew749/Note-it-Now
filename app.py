from flask import Flask,jsonify, Response, session, request, redirect, render_template
import flask
import requests
# import dropbox
import json
import pdb
import base64
# from dropbox.client import DropboxOAuth2Flow, DropboxClient
from base64 import decodestring
from ocr import *
import uuid

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def authenticate():
    return render_template("index.html")

@app.route('/main')
def mainView():
    if("access_token" in session):
        return render_template('main.html')
    else:
        return redirect("/")

@app.route('/upload',methods=['POST'])
def spliceImage():
    if request.method =='POST':
        data = request.form['image']
        tempFileName = "static/temp/"+str(uuid.uuid4())
        decode64String(tempFileName,data);
        images=segmenter.getImages(tempFileName)
        return json.dumps(images)
    return "fail"


def decode64String(filename,imagestr):
    with open(filename,"wb") as f:
        f.write(decodestring(imagestr))
    return filename

def get64String(filename):
    with open(filename, "rb") as image_file:
       encoded_string = base64.b64encode(image_file.read())
    return encoded_string

@app.route('/files', methods=['POST'])
def filesView():
    if("access_token" in session):
        return flask.jsonify(**{ "didstuff": True })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
