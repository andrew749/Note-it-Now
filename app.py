import sys
import os
from flask import Flask, url_for, jsonify, Response, session, request, redirect, render_template
import flask
import json
import base64
import uuid
from flask_oauthlib.client import OAuth
import credentials

from ocr import *

app = Flask(__name__, static_url_path='/static')

app.config['GOOGLE_ID'] = credentials.client_id
app.config['GOOGLE_SECRET'] = credentials.client_secret
app.secret_key = "dev"

oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={'scope':'email'},
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@app.route('/login')
def login():
    return google.authorize(callback=url_for('authorized', _external=True))

@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    # return jsonify({"data": me.data})
    return redirect(url_for('main'))

@app.route('/')
def authenticate():
    return render_template("index.html")

@app.route('/main')
def main():
    if("google_token" in session):
        return render_template('main.html')
    else:
        return redirect("/")

#endpoint to accept image upload
@app.route('/upload', methods=['POST'])
def spliceImage():
    if request.method == 'POST':
        data = request.form['image']
        tempFileName = "static/temp/"+str(uuid.uuid4())
        decode64String(tempFileName,data);
        images = segmenter.getImages(tempFileName)
        return json.dumps(images)
    return "fail"

#helper function to decode the image from the import client
def decode64String(filename, imagestr):
    with open(filename,"wb") as f:
        f.write(base64.b64decode(imagestr))
    return filename

#helper function to encode to 64bit to send to a client
def get64String(filename):
    with open(filename, "rb") as image_file:
       encoded_string = base64.b64encode(image_file.read())
    return encoded_string

@app.route("/logout")
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@app.route('/files', methods=['POST'])
def filesView():
    if("access_token" in session):
        return flask.jsonify(**{ "didstuff": True })

#run the server
if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0', port = 5000)
