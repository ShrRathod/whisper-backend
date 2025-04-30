import os
import tempfile
from flask import Flask, request, jsonify, render_template
import whisper

app = Flask(__name__)
model = whisper.load_model("base")  # or "small", "medium", etc.

@app.route("/")
def home():
    return render_template("index.html")  # Serve frontend

@app.route("/upload", methods=["POST"])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp:
        file.save(temp.name)
        result = model.transcribe(temp.name)

    transcription = result["text"]
    return jsonify({"transcription": transcription})

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    transcript = data.get("transcript")
    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400

    summary = transcript[:150] + "..." if len(transcript) > 150 else transcript
    return jsonify({"summary": summary})

@app.route("/identify-speakers", methods=["POST"])
def identify_speakers():
    data = request.get_json()
    transcript = data.get("transcript")
    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400

    fake_speakers = [
        {"speaker": "Speaker 1", "text": transcript[:len(transcript)//2]},
        {"speaker": "Speaker 2", "text": transcript[len(transcript)//2:]},
    ]
    return jsonify({"speakers": fake_speakers})

@app.route("/feedback", methods=["POST"])
def collect_feedback():
    data = request.get_json()
    feedback = data.get("feedback")
    if not feedback:
        return jsonify({"error": "No feedback provided"}), 400

    print("Received feedback:", feedback)
    return jsonify({"message": "Feedback received!"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
