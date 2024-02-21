#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', strict_slashes=True, methods=['GET'])
def get_route():
    """get function"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")