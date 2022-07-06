from distutils.log import debug
from flask import Flask, send_from_directory,request
from flask_cors import CORS

from pathlib import Path
from datetime import datetime, timedelta

media_base_path = Path("/files")

app = Flask(__name__)

CORS(app)

@app.route('/<path:path>')
def download_file(path):
    print(path)
    return send_from_directory(media_base_path,path)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0",port=6001,debug=True)