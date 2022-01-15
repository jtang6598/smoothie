import time
import aiohttp
import getpass
import urllib
import os

from spotify.gateway import spotify_post

class AuthorizationHandler:

    spotify_client_id = None
    spotify_client_secret = None

    def __init__(self, client_session, redirect_uri=None):
        self._client_session = client_session

        if not AuthorizationHandler.spotify_client_id:
            try:
                AuthorizationHandler.spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
            except KeyError:
                AuthorizationHandler.spotify_client_id = getpass.getpass(prompt="Client ID: ")
        if not AuthorizationHandler.spotify_client_secret:
            try: 
                AuthorizationHandler.spotify_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
            except KeyError:
                AuthorizationHandler.spotify_client_secret = getpass.getpass(prompt="Client Secret: ")

        self._auth = aiohttp.BasicAuth(AuthorizationHandler.spotify_client_id, AuthorizationHandler.spotify_client_secret)

        if redirect_uri:
            self._redirect_uri = redirect_uri
        else: 
            self._redirect_uri = 'https://google.com'


    async def user_authorize(self):
        params = {
            'client_id': self.spotify_client_id,
            'response_type': 'code',
            'redirect_uri':  urllib.parse.quote_plus(self._redirect_uri), 
            'state': 'dummy_auth',
            'scope': None
        }
        response = self._client_session.get(url="https://accounts.spotify.com/authorize", params=params)
        pass


    async def request_access_token(self, user):
        body = {
            'grant_type': 'authorization_code',
            'code': user.code,
            'redirect_uri': self._redirect_uri
        }

        response = await spotify_post(self._client_session, api="/api/token", base_url="https://accounts.spotify.com", body=body, auth=self._auth, isjson=False)
        user.access_token = response['access_token']
        user.refresh_token = response['refresh_token']
        user.token_expiration_time = int(time.time()) + response['expires_in']

        return response


    async def refresh_access_token(self, user):
        body = {
            'grant_type': 'refresh_token',
            'refresh_token': user.refresh_token
        }

        response = await spotify_post(self._client_session, api="/api/token", base_url="https://accounts.spotify.com/api/token", body=body, auth=self._auth, isjson=False)
        user.access_token = response['access_token']
        user.token_expiration_time = int(time.time()) + response['expires_in']

        try:
            user.refresh_token = response['refresh_token']
        except KeyError:
            user.refresh_token = None

        return response

