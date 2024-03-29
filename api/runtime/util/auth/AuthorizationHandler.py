from typing import Any, Dict
from python_settings import settings 
import aiohttp
import os

from util.spotify.gateway import spotify_post

class AuthorizationHandler:

    @staticmethod
    async def request_access_token(
        client_session: aiohttp.ClientSession,
        code: str, 
        redirect_uri: str,
    ) -> Dict[str, Any]:
        body = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri
        }

        auth = aiohttp.BasicAuth(os.environ.get("SPOTIFY_CLIENT_ID"), os.environ.get("SPOTIFY_CLIENT_SECRET"))

        response = await spotify_post(client_session, api="/api/token", base_url=settings.SPOTIFY_AUTH_API, body=body, auth=auth, isjson=False)

        return response


    @staticmethod
    async def refresh_access_token(
        client_session: aiohttp.ClientSession,
        refresh_token: str,
    ) -> Dict[str, Any]:
        body = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }

        auth = aiohttp.BasicAuth(os.environ.get("SPOTIFY_CLIENT_ID"), os.environ.get("SPOTIFY_CLIENT_SECRET"))

        response = await spotify_post(client_session, api="/api/token", base_url=settings.SPOTIFY_AUTH_API, body=body, auth=auth, isjson=False)

        return response

