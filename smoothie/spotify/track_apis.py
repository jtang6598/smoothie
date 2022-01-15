

from spotify.gateway import spotify_get


async def get_audio_features_for_several_tracks(session, user, track_ids):
    # len(track_ids) must be <= 100
    headers = user.build_auth_header(session)
    try:
        params = { 'ids': ','.join(track_ids) }
    except TypeError as te:
        print('Track ids:\t' + str(track_ids))
        raise te

    response = await spotify_get(session, '/audio-features', params=params, headers=headers)

    return response['audio_features']
