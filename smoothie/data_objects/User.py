from dataclasses import dataclass
import time
from traceback import print_stack
from typing import Optional

from auth.AuthorizationHandler import AuthorizationHandler
from aiohttp import ClientSession

@dataclass
class User:
    code: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token:  Optional[str] = None
    user_id: Optional[str] = None
    display_name: Optional[str] = None
    token_expiration_time: Optional[int] = None

    async def check_and_refresh_token(
        self, 
        session: ClientSession
    ):
        if self.token_expiration_time < int(time.time()):
            if not self.refresh_token:
                print(f'User {self.user_id} tried refreshing access token with no refresh token! Exiting...')
                print_stack()
                return
            response = await AuthorizationHandler.refresh_access_token(session, self.refresh_token)
            self.access_token = response['access_token']
            self.token_expiration_time = int(time.time()) + response['expires_in']
            try:
                self.refresh_token = response['refresh_token']
            except KeyError:
                self.refresh_token = None

    async def build_auth_header(
        self, 
        session: ClientSession
    ):
        await self.check_and_refresh_token(session)
        return { 
            'Authorization': 'Bearer ' + self.access_token,
            'content-type': 'application/json' 
        }
        