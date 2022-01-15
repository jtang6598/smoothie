from spotify.gateway import spotify_get


async def get_current_users_playlists(session, user):
    headers = user.build_auth_header(session)
    
    response = await spotify_get(session, 'https://api.spotify.com/v1/me/playlists', headers=headers)
    playlist_list = response['items']
    while 'next' in response and response['next']:
        response = await spotify_get(session, response['next'], headers=headers)
        playlist_list += response['items']

    return playlist_list


async def get_playlist(session, user, playlist_id):
    headers = user.build_auth_header(session)

    params = {
        'fields': 'items(added_at, track(id)),next' # only return specific fields of the response
    }

    response = await spotify_get(session, f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=headers, params=params)
    playlist = response['items']

    # print(response)
    # print(playlist)

    while 'next' in response and response['next']:
        # print(response)
        response = await spotify_get(session, response['next'], headers=headers, params=params)
        playlist += response['items']

    return playlist