#!/usr/bin/env python3
"""
class to manage the API authenctication
"""

from flask import request
from typing import List, TypeVar
from re import match, sub


class Auth:
    """
    class to manage the API authenication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """public method"""
        if path is None:
            return True
        elif excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if excluded_path[-1] == '*':
                sub('*', '.*')
            if path.rstrip('/') == excluded_path.rstrip('/') or\
                    match(excluded_path, path):
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
