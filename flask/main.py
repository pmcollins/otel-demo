from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({"library": "flask"})


app.run(port=8002, host='0.0.0.0')

