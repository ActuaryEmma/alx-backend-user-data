#!/usr/bin/env python3
"""
Hash password
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str):
        """ methods that takes in a string arg and returns bytes
        bcrypt.hashpw:create the final hash stored in db takes(pass, salt) arg
        bcrypt.gensalt() - generate salt
        """
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hashed

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
                hashed_password = self._hash_password(password)
                new_user = self._db.add_user(email, hashed_password)
                return new_user
            except ValueError:
                raise ValueError("User <user's email> already exists")
        else:
            raise ValueError(f"User {email} already exists")

    # def register_user(self, email: str, password: str):
        #     """
        #     """
        #     user = self._db.find_user_by(email=email)
        #     print("******")
        #     print(user)
        #     print("*******")
        #     try:
        #         if user is None:
        #             hashed_password = self._hash_password(password)
        #             new_user = self._db.add_user(email, hashed_password)
        #             return new_user
        #     except ValueError:
        #         raise ValueError("User <user's email> already exists")
