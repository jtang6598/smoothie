from api.runtime.util.spotify.gateway import spotify_get
from api.runtime.util.data_objects.User import User
from aiohttp import ClientSession

async def get_profile(
    session: ClientSession, 
    user: User
):
    headers = await user.build_auth_header(session)

    response = await spotify_get(session, '/me', headers=headers)

    return response

