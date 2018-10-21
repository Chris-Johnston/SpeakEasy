from flask import Flask, jsonify, request, flash, redirect, render_template
from werkzeug.utils import secure_filename
import json
import configparser
import os
import base64
import time
import subprocess
import random

from google.cloud import storage
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

config = configparser.ConfigParser()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ['jpg', 'wav', 'mp3', 'png', 'flac', 'ogg']


with open('config.ini') as cfg:
    config.read_string(cfg.read())


@app.route('/')
def tester():
    return render_template('record.html')


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

@app.route('/phrases/random', methods=['GET'])
def get_random():
    """
    Returns a random phrase
    :return:
    """
    try:
        with open('phrases.json') as json_data:
            # load the contents as a json object
            data = json.load(json_data)
            # get the index in the list
            return jsonify(random.choice(data))
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

        # standardize the format of the file
        #os.execl('avconf', '-i', str(path), '-map', '0:a', '-codec:a', 'opus', '-b:a', '100k', '-vbr', 'on', 'file.opus')

        # res = os.execl('/usr/bin/opusenc', '--downmix-mono', '--raw-rate', '48000', str(path), os.path.join(temp_dir, 'file.opus'))

        # cmd = 'avconf -i ' + path + ' -f wav - | /usr/bin/opusenc --downmix-mono --raw-rate 48000 - ' + os.path.join(temp_dir, 'file.opus')
        cmd = 'ffmpeg -y -i ' + path + ' -ar 48000 -ac 1 ' + os.path.join(temp_dir, 'file.flac')

        # cmd = "/usr/bin/opusenc --downmix-mono --raw-rate 48000" + path + " " + os.path.join(temp_dir, 'file.opus')
        subprocess.call(cmd, shell=True)

        path = os.path.join(temp_dir, 'file.flac')

        # return the path for now, need to have this call the google
        # apis

        # ok, now I get to interface w/ google cloud platform
        storage_client = storage.Client()
        # get the bucket to upload to
        b = storage_client.get_bucket('dubhacks2018speechrecordings')
        # blob = b.blob(filename)
        blob = b.blob('file.flac')
        blob.upload_from_filename(path)

        url = blob.public_url

        time.sleep(2)

        bucket_uri = 'gs://dubhacks2018speechrecordings/' + 'file.flac'

        # return bucket_uri
        speech_client = speech.SpeechClient()
        cc = types.RecognitionConfig(encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
                                     sample_rate_hertz=48000,
                                         language_code='en-US')

        # return bucket_uri

        response = speech_client.recognize(cc, audio={'uri': bucket_uri})

        #with open(path, encoding = "ISO-8859-1") as aaa:
        #    b64 = base64.b64encode(aaa.read().encode('ISO-8859-1'))
            # return b64

        #response = speech_client.recognize(cc, audio={'content': b64})


        #return jsonify(dir(response))
        #return response.MergeFromString
        # output = "output is:\n"
        #
        # for result in response.results:
        #     output += result.alternatives[0].transcript + '\n'

        if len(response.results) > 0:
            return response.results[0].alternatives[0].transcript
        return "No audio."

        # return path
    return "error"

# debugging use only
if __name__ == '__main__':
    app.run()