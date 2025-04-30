from flask import Flask, request, jsonify
import whisper
import os
import tempfile

app = Flask(__name__)
model = whisper.load_model("base")  # use "tiny" if base is too slow

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    audio_file = request.files['file']
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp:
        audio_file.save(temp.name)
        result = model.transcribe(temp.name)
        os.remove(temp.name)

    # Replace with your own logic later
    summary = result['text'][:200]
    keywords = [word for word in result['text'].split()[:5]]
    sentiment = "Neutral"

    return jsonify({
        'summary': summary,
        'keywords': keywords,
        'sentiment': sentiment
    })

if __name__ == '__main__':
    app.run()
