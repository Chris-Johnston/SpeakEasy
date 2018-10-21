from flask import Flask, jsonify, request, flash, redirect
from werkzeug.utils import secure_filename
import json
import configparser
import os

from google.cloud import storage
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

app = Flask(__name__)

config = configparser.ConfigParser()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['jpg', 'wav', 'mp3', 'png', 'flac']


with open('config.ini') as cfg:
    config.read_string(cfg.read())

@app.route('/')
def index():
    # debugging
    # file = config.get('Files', 'tempdir')
    # print(file)
    return 'Test index, please ignore'


@app.route('/phrases/<int:phrase>', methods=['GET'])
def get_phrase(phrase: int):
    """
    Reads from the phrases json and returns the specific matching
    phrase, or returns the default phrase

    :return:
    """
    try:
        with open('phrases.json') as json_data:
            # load the contents as a json object
            data = json.load(json_data)
            # get the index in the list
            return jsonify(data[phrase])
    except IndexError:
        return "Out of range", 404
    except ValueError:
        return "Out of range", 404


@app.route('/phrases', methods=['GET'])
def allphrases():
    """
    Reads from the phrases json file and returns the entire contents
    :return:
    """
    # open the phrases file and just return it, don't
    # have to do anything fancy with the contents
    with open('phrases.json') as json_data:
        return jsonify(json.load(json_data))

@app.route('/sound', methods=['POST'])
def upload_sound():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('no selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        temp_dir = config['Files']['tempdir']
        path = os.path.join(temp_dir, filename)
        file.save(path)
        # return the path for now, need to have this call the google
        # apis

        # ok, now I get to interface w/ google cloud platform
        storage_client = storage.Client()
        # get the bucket to upload to
        b = storage_client.get_bucket('dubhacks2018speechrecordings')
        blob = b.blob(filename)
        blob.upload_from_filename(path)

        url = blob.public_url

        bucket_uri = 'gs://dubhacks2018speechrecordings/' + filename

        speech_client = speech.SpeechClient()
        cc = types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
                                         language_code='en-US')

        # return bucket_uri

        response = speech_client.recognize(cc, audio={'uri': bucket_uri})
        #return jsonify(dir(response))
        #return response.MergeFromString
        output = ""

        for result in response.results:
            output += result.alternatives[0].transcript + '\n'

        return output

        # return path
    return "error"

# debugging use only
if __name__ == '__main__':
    app.run()