from multiprocessing.connection import answer_challenge
from flask import Flask
from flask import request
from flask_cors import CORS
from flask_api import status
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
def compare_text():
    req = request.json

    if "user_answer" not in req or "correct_answer" not in req:
        return (
            json.dumps(
                {
                    "error": "correct_answer and user_answer must be defined and must be strings"
                }
            ),
            status.HTTP_400_BAD_REQUEST,
        )

    if (
        isinstance(req["user_answer"], str) is False
        or isinstance(req["correct_answer"], str) is False
    ):
        return (
            json.dumps({"error": "correct_answer and user_answer must be strings"}),
            status.HTTP_400_BAD_REQUEST,
        )

    comparison = TextComparison(req["user_answer"], req["correct_answer"])
    answer = comparison.check_answer()
    return json.dumps({"answer": answer}), status.HTTP_200_OK


if __name__ == "__main__":
    app.run(host="'127.0.0.1'", port=8080, debug=True)
