from dataclasses import dataclass
import time
from typing import Optional

from auth.AuthorizationHandler import AuthorizationHandler

@dataclass
class User:
    code: str = None
    access_token: str = None
    refresh_token:  str = None
    user_id: str = None
    token_expiration_time: int = None

    def check_and_refresh_token(self, session):
        if self.token_expiration_time < int(time.time()):
            if not self.refresh_token:
                print('REFRESHING ACCESS TOKEN WITH NO REFRESH TOKEN!')
            auth_handler = AuthorizationHandler(session)
            auth_handler.refresh_access_token(self)

    def build_auth_header(self, session):
        self.check_and_refresh_token(session)
        return { 'Authorization': 'Bearer ' + self.access_token }
        