#!/usr/bin/env python3
"""
class to manage the API authenctication
"""

from flask import request
from typing import List, TypeVar


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
            if path.rstrip('/') == excluded_path.rstrip('/'):
                return False
        return False

    def authorization_header(self, request=None) -> str:
        """public method"""
        if request is None:
            return None
        if Authorization not in request:
            return None
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ public method"""
        return None
