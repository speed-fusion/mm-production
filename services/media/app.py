from flask import Flask, send_from_directory,request
from flask_cors import CORS

from pathlib import Path
from datetime import datetime, timedelta

media_base_path = Path("/files")

app = Flask(__name__)

CORS(app)

@app.route('/')
def download_file():
    file_path = request.path
    return send_from_directory(media_base_path,file_path)