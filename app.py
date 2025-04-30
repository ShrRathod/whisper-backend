import os
import tempfile
from flask import Flask, request, jsonify
import whisper

app = Flask(__name__)
model = whisper.load_model("base")  # You can change to 'small', 'medium', etc.

@app.route('/')
def home():
    return "Whisper backend is live!"

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            file.save(temp_audio.name)
            result = model.transcribe(temp_audio.name)
            os.remove(temp_audio.name)

        return jsonify({'transcription': result['text']})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
