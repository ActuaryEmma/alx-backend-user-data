#!/usr/bin/env python3
"""
Hash password
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ methods that takes in a string arg and returns bytes
    """
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """init function"""
        self._db = DB()

    def register_user(self, email: str, password: str):
        """
        Register a new user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            try:
                hashed_password = _hash_password(password)
                new_user = self._db.add_user(email, hashed_password)
                return new_user
            except ValueError:
                raise ValueError("User <user's email> already exists")
        else:
            raise ValueError(f"User {email} already exists")