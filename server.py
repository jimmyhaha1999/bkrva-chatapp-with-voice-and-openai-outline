import base64
import json
import os
from flask import Flask, render_template, request
from flask_cors import CORS

from worker import (
    speech_to_text as stt,
    text_to_speech,
    openai_process_message
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print("processing speech-to-text")

    audio_binary = request.data
    text = stt(audio_binary)

    response = app.response_class(
        response=json.dumps({'text': text}),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/process-message', methods=['POST'])
def process_prompt_route():
    user_message = request.json['userMessage']
    voice = request.json['voice']

    print('user_message', user_message)
    print('voice', voice)

    openai_response_text = openai_process_message(user_message)

    openai_response_text = os.linesep.join(
        [s for s in openai_response_text.splitlines() if s]
    )

    openai_response_speech = text_to_speech(openai_response_text, voice)

    openai_response_speech = base64.b64encode(openai_response_speech).decode('utf-8')

    response = app.response_class(
        response=json.dumps({
            "openaiResponseText": openai_response_text,
            "openaiResponseSpeech": openai_response_speech
        }),
        status=200,
        mimetype='application/json'
    )

    return response


if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
