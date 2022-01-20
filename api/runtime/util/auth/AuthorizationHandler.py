from typing import Any, Dict
import aiohttp
import os

from api.runtime.util.spotify.gateway import spotify_post

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

        response = await spotify_post(client_session, api="/api/token", base_url="https://accounts.spotify.com", body=body, auth=auth, isjson=False)
AQCt_rAn4YHE5FX_jtqG9ONdv5K5fZi3nfaW9l1B2c_bv6Y1j8LCMcCEXOtgJSryzAdHOgFWcJP55ciwRtPwJdGKD2Jx77bBlv7Ct0Ihsv1tn7GbdLa2USBHxg_6ooqV8rCFW7Vl_8zqJXR_Wf5mARLku7PfnHz_Tt-8AgAdLne-pe6fUbFJOPWZmmr6s0ebVBMvtHCUZeNQNlO62JQcl_cdsayw

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

        response = await spotify_post(client_session, api="/api/token", base_url="https://accounts.spotify.com/api/token", body=body, auth=auth, isjson=False)

        return response

