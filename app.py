import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Whisper backend is live!"

if __name__ == "__main__":
    # Get the port from the environment variable, Render provides this automatically
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT is not set
    app.run(host="0.0.0.0", port=port)  # Bind to 0.0.0.0 to make it accessible externally
