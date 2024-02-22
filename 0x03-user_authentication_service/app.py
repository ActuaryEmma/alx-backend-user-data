#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=True, methods=['GET'])
def get_route():
    """get function"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', strict_slashes=True, methods=['POST'])
def post_user():
    """post route"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', strict_slashes=True, methods=['POST'])
def login() -> str:
    """login function"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        AUTH.create_session(email=email)
        return jsonify({"email": email, "message": "logged in"})
    abort(401)


@app.route('/sessions', strict_slashes=True, methods=['DELETE'])
def logout() -> str:
    """logout session"""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', strict_slashes=True, methods=['GET'])
def profile():
    """user profile"""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
