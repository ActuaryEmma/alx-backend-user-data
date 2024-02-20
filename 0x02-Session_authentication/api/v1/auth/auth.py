#!/usr/bin/env python3
"""
class to manage the API authenctication
"""

from flask import request
from typing import List, TypeVar
from re import match, sub
import os


class Auth:
    """
    class to manage the API authenication
    """

    def __init__(self):
        """init function"""
        self.session_name = os.environ.get('SESSION_NAME', '_my_session_id')

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method"""
        if path is None:
            return True
        elif excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if path.rstrip('/') == excluded_path.rstrip('/') or\
                    (match(sub(r"\*", ".*", excluded_path), path)):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """public method"""
        if request is None:
            return None
        headers = request.headers
        return headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ public method"""
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        return request.cookies.get(os.environ.get(
            'SESSION_NAME', 
            '_my_session_id'))
