#!/usr/bin/env python3
"""
Create a new Flask view that handles all routes for the Session authentication
"""
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify
import os


@app_views.route('/auth_session/login', strict_slashes=False, methods=['POST'])
def post_session():
    """post a session"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    if not users[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    value_session = auth.create_session(users[0].id)
    response = jsonify(users[0].to_json())
    response.set_cookie(os.getenv('SESSION_NAME'), value_session)
    return response
