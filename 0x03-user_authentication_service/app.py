#!/usr/bin/env python3
"""Basic Flask app"""
from flask import Flask, jsonify, request, abort, redirect
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
        session_id = AUTH.create_session(email=email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    abort(401)


@app.route('/sessions', methods=['DELETE'])
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


@app.route('/profile', methods=['GET'])
def profile():
    """user profile"""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """reset a password token"""
    try:
        email = request.form.get('email')
    except KeyError:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email=email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
