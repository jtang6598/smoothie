from auth.AuthorizationHandler import AuthorizationHandler
from spotify.gateway import *

async def get_profile(session, user):
    headers = user.build_auth_header(session)

    response = await spotify_get(session, 'https://api.spotify.com/v1/me', headers=headers)
    user.user_id = response['id']

    return response

