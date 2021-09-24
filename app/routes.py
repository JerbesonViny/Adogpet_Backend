from flask.json import jsonify
from app import app

@app.route('/', methods=['GET',])
def home():
  return jsonify(message="Hello world")