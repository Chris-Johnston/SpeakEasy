from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
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

# debugging use only
if __name__ == '__main__':
    app.run()