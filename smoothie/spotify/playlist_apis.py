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
        'fields': 'tracks.items(added_at, track(id)),tracks.next,name' # only return specific fields of the response
    }

    response = await spotify_get(session, f'https://api.spotify.com/v1/playlists/{playlist_id}', headers=headers, params=params)
    playlist = response['tracks']['items']

    # print(response)
    # print(playlist)

    try:
        while 'next' in response['tracks'] and response['tracks']['next']:
            # print(response)
            response_tmp = await spotify_get(session, response['tracks']['next'], headers=headers, params=params)
            try:
                playlist += response_tmp['tracks']['items']
            except KeyError as ke:
                print('Previous response.tracks.next:\t' + response['tracks']['next'])
                print('Previous response:\t' + str(response))
                raise ke

            if not response_tmp:
                print('Previous response:\t' + str(response))
                print('This response:\t' + str(response_tmp))

            response = response_tmp
    except KeyError as ke:
        print('Response used to enter loop:\t' + str(response))
        raise ke

    return playlist