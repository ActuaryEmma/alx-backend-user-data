#!/usr/bin/env python3
"""
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os

class SessionExpAuth(SessionAuth):
    """
    """
    def __init__(self):
        """"""
        self.session_duration = os.getenv('SESSION_DURATION', 0)
        try:
            self.session_duration = int(self.session_duration)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """create a sessionID by calling super()
        supper will call the create_session() method of SessionAuth
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
                }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """"""
        if session_id is None:
            return None
        if self.user_id_by_session_id[session_id] == None:
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict.get('user_id')
        if session_dict.get('created_at') == None:
            return None
        created_at = session_dict.get('created_at')
        expiration_date = created_at + timedelta(seconds=self.session_duration)
        current_time = datetime.now()
        if expiration_date < current_time:
            return None
        return session_dict.get('user_id')
