import os
from flask import Flask, request, jsonify
import whisper
import torch
import uuid

app = Flask(__name__)

# Load Whisper model once at startup
device = "cuda" if torch.cuda.is_available() else "cpu"
model = whisper.load_model("base", device=device)

# Store feedback temporarily in memory (you can later move to a database)
feedback_store = []

@app.route('/')
def home():
    return "Whisper backend is live!"

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    filename = f"temp_{uuid.uuid4()}.mp3"
    audio_path = os.path.join("/tmp", filename)
    audio_file.save(audio_path)

    try:
        result = model.transcribe(audio_path)
        text = result.get("text", "")
        os.remove(audio_path)

        # Generate a dummy summary (you can integrate a better summarizer later)
        summary = text[:200] + "..." if len(text) > 200 else text

        return jsonify({
            "transcription": text,
            "summary": summary,
            "speakers": ["Speaker 1", "Speaker 2"],  # Placeholder
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['POST'])
def collect_feedback():
    data = request.get_json()
    feedback = {
        "rating": data.get("rating"),
        "comment": data.get("comment"),
    }
    feedback_store.append(feedback)
    return jsonify({"message": "Feedback received!"}), 200

@app.route('/feedback', methods=['GET'])
def get_feedback():
    return jsonify(feedback_store), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
