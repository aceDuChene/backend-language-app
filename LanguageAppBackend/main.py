from multiprocessing.connection import answer_challenge
from flask import Flask
from flask import request
from flask_cors import CORS
from google.cloud import speech_v1 as speech
from text_comparison import *
import json

app = Flask(__name__)

CORS(app)


@app.route("/audio/<language_code>", methods=["POST"])
def process_audio(language_code):
    content = request.get_data()

    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.AMR_WB,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)

    if response.results:
        transcription = response.results[0].alternatives[0].transcript
        return json.dumps({"text": transcription}), 200
    else:
        return json.dumps({"text": "Audio Not detected. Try Again."}), 400

@app.route("/text-comparison", methods=["POST"])
def check_answer():
    req = request.json
    comparison = TextComparison(req["user_answer"], req["correct_answer"])
    answer = comparison.check_answer()
    return json.dumps({"answer": answer })


if __name__ == "__main__":
    app.run(host="localhost", port=8090, debug=True)
