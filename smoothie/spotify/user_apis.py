from auth.AuthorizationHandler import AuthorizationHandler
from spotify.gateway import *
from aiohttp import ClientSession
from smoothie.data_objects.User import User

async def get_profile(
    session: ClientSession, 
    user: User
):
    headers = await user.build_auth_header(session)

    response = await spotify_get(session, '/me', headers=headers)

    return response

