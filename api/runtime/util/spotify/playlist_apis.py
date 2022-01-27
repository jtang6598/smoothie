from typing import List
from util.spotify.gateway import spotify_get, spotify_post
from aiohttp import ClientSession
from util.data_objects.User import User
from python_settings import settings 


async def get_current_users_playlists(
    session: ClientSession, 
    user: User
):
    headers = await user.build_auth_header(session)
    
    response = await spotify_get(session, '/me/playlists', headers=headers)
    playlist_list = response['items']
    while 'next' in response and response['next']:
        response = await spotify_get(session, response['next'], headers=headers, base_url="")
        playlist_list += response['items']

    return playlist_list


async def get_playlist(
    session: ClientSession, 
    user: User, 
    playlist_id: str
):
    headers = await user.build_auth_header(session)

    params = {
        'fields': 'items(added_at, track(id)),next' # only return specific fields of the response
    }

    response = await spotify_get(
        session, 
        f'/playlists/{playlist_id}/tracks', 
        headers=headers, 
        params=params
    )
    playlist = response['items']

    # print(response)
    # print(playlist)

    while 'next' in response and response['next']:
        # print(response)
        response = await spotify_get(session, response['next'], headers=headers, params=params, base_url="")
        playlist += response['items']

    return playlist


async def create_playlist(
    session: ClientSession,
    user: User,
    name: str,
    public: bool = True,
    collaborative: bool = False,
    description: str = ""
):
    headers = await user.build_auth_header(session)
    body = {
        "name": name,
        "public": public,
        "collaborative": collaborative,
        "description": description
    }

    response = await spotify_post(
        session, 
        f"/users/{user.user_id}/playlists", 
        headers=headers, 
        body=body
    )

    return response['id']


async def add_to_playlist(
    session:  ClientSession,
    user: User,
    playlist_id: str,
    song_uris: List[str]
):
    max_uris_per_request = 100
    uri_chunks = [song_uris[i: i + max_uris_per_request] for i in range(0, len(song_uris), max_uris_per_request)]
    headers = await user.build_auth_header(session)

    for uri_chunk in uri_chunks:
        body = {
            "uris": uri_chunk
        }
        await spotify_post(session, f"/playlists/{playlist_id}/tracks", headers=headers, body=body)
    pass
