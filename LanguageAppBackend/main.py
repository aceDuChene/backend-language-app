from flask import Flask
from flask import request
from flask_cors import CORS
import json
from google.cloud import speech_v1 as speech
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pyxdameraulevenshtein import damerau_levenshtein_distance

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
    user_answer = request.json["user_answer"]
    correct_answer = request.json["correct_answer"]
    print(user_answer)
    print(correct_answer)
    return correct_answer


if __name__ == "__main__":
    app.run(host="localhost", port=8090, debug=True)
