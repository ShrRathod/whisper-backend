from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import whisper
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the tiny Whisper model once at startup
model = whisper.load_model("tiny")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    print("Received transcription request.")

    if 'audio' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    print(f"Saved file to {filepath}")

    # Transcribe audio using the global model
    result = model.transcribe(filepath)
    print("Transcription complete.")
    return jsonify({'transcription': result['text']})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Use dynamic port if provided (for Render)
    app.run(debug=False, host='0.0.0.0', port=port, threaded=True)
