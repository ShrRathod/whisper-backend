from flask import Flask, request, jsonify, render_template
import whisper
import os

app = Flask(__name__)

# Use lighter model for limited resources
model = whisper.load_model("tiny")

@app.route('/')
def index():
    return render_template('index.html')  # Correctly serve from templates folder

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    audio_path = os.path.join("temp", audio_file.filename)
    os.makedirs("temp", exist_ok=True)
    audio_file.save(audio_path)

    try:
        result = model.transcribe(audio_path)
        return jsonify({'transcription': result['text']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(audio_path)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get("text", "")
    summary = f"(Mock summary for): {text[:50]}..."
    return jsonify({"summary": summary})

@app.route('/identify-speakers', methods=['POST'])
def identify_speakers():
    data = request.get_json()
    text = data.get("text", "")
    speakers = [{"speaker": "Speaker 1", "text": text}]
    return jsonify({"speakers": speakers})

@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    print("Received feedback:", data)
    return jsonify({"status": "Feedback received"})

@app.route('/routes')
def list_routes():
    return jsonify([str(rule) for rule in app.url_map.iter_rules()])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
