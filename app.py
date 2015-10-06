import sys
import os
sys.path.insert(1, os.path.join(os.path.abspath("bin/lib/python2.7/site-packages")))
from flask import Flask,jsonify, Response, session, request, redirect, render_template
import flask
import requests
import json
import base64
from base64 import decodestring
import uuid

from ocr import *

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

#endpoint to accept image upload
@app.route('/upload',methods=['POST'])
def spliceImage():
    if request.method =='POST':
        data = request.form['image']
        tempFileName = "static/temp/"+str(uuid.uuid4())
        decode64String(tempFileName,data);
        images=segmenter.getImages(tempFileName)
        return json.dumps(images)
    return "fail"

#helper function to decode the image from the import client
def decode64String(filename,imagestr):
    with open(filename,"wb") as f:
        f.write(decodestring(imagestr))
    return filename

#helper function to encode to 64bit to send to a client
def get64String(filename):
    with open(filename, "rb") as image_file:
       encoded_string = base64.b64encode(image_file.read())
    return encoded_string

@app.route('/files', methods=['POST'])
def filesView():
    if("access_token" in session):
        return flask.jsonify(**{ "didstuff": True })

#run the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
