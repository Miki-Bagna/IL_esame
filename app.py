from flask import Flask, jsonify, request
from flask_cors import CORS
from emotions.extractions import characters_extraction, characters_sentences_extraction
from emotions.emotions import process_emotion
from summary.summarymodel import clean4sum , summarize
import requests
import json

# API
url = "https://api.meaningcloud.com/summarization-1.0"

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/ping', methods=['GET'])
def check():
    return "Pong"

@app.route('/upload', methods=['POST'])
def process_text():
    response_object = {'status': 'error'}

    if request.method == 'POST':
        if 'file' not in request.files:
            response_object['message'] = 'No file part'
            return jsonify(response_object), 400

        file = request.files['file']

        if file.filename == '':
            response_object['message'] = 'No selected file'
            return jsonify(response_object), 400

        if file and file.filename.endswith('.txt'):
            content = file.read().decode('utf-8')

            # estrazione personaggi
            characters = characters_extraction(content)
            
            # estrazione frasi per quei personaggi
            characters_sentences = {}
            for character in characters:
                sentences = characters_sentences_extraction(content, character)
                if len(sentences) > 1:
                    emotions = process_emotion(sentences)
                    if len(emotions) >= 1:
                        characters_sentences[character] = []
                        for emotion_label in emotions:
                            characters_sentences[character].append(emotion_label)




            response_object = {'status': 'success', 'characters_sentences': characters_sentences}
            return jsonify(response_object), 200

        else:
            response_object['message'] = 'Invalid file format'
            return jsonify(response_object), 400

    return jsonify(response_object), 405


@app.route('/up_summ', methods=['POST'])
def summarization():
    response_object_sum = {'status': 'error'}

    if request.method == 'POST':

        file = request.files['file']

        
        if file and file.filename.endswith('.txt'):
            content = file.read().decode('utf-8')

            # divisione in scene
            batches = clean4sum(content)
            #riassunto
            script_summary = summarize(batches)

            # API
            payload={
                'key': 'd19cb8e2968cedde612e615168c012e2',
                'txt': script_summary,
                'sentences': 10
            }

            response = requests.post(url, data=payload)
            response_data = response.json()
            response_data = json.dumps(response_data['summary'])
            response_data = response_data.replace("[...]", "")

            print(response_data)

            response_object_sum = {'status': 'success', 'script_summary': response_data}
            
            return jsonify(response_object_sum), 200

        else:
            response_object_sum['message'] = 'Invalid file format'
    
    return jsonify(response_object_sum), 405


if __name__ == '__main__':
    app.run()