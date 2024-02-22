#!/usr/bin/env python3
"""
Hash password
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """ methods that takes in a string arg and returns bytes
    """
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """return a string represenation of a new UUID"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """init function"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
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

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials Validation"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        password = password.encode('utf-8')
        user_password = user.hashed_password
        if bcrypt.checkpw(password, user_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """
        find user corresponding to the email, generate UUID and store in DB
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user:
            user_uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=user_uuid)
            return user_uuid
        return None

    def get_user_from_session_id(self, session_id: str) -> User or None:
        """find user by session_id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """destroy a session"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        self._db.update_user(user.id, session_id=None)
        return None
