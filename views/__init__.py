from flask import render_template
from app import app
from model import *


@app.route('/', methods=["GET"])
def home():
    return render_template('index.html')

# To start the BG task in new thread of getting new videos
@app.before_first_request
def before_first_request_func():
    run()

# If no args passed then deafults to 1
@app.route('/latestVids', methods=["GET"])
def latestVideos():
    return fetchPage()

# if no args found default to India as search Query
@app.route('/searchDB', methods=["GET"])
def searchDb():
    return search()