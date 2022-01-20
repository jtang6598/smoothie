from runtime.util.data_objects.User import User
from runtime.util.spotify import user_apis, playlist_apis
import aiohttp
import asyncio

def test_spotify_get():
    me = User(code='AQCOwTp2S9niCD_zIuia0x5gVWMnXwTlSSKMiqKKjP9u7jgIikCrmshKwqA1NsIIHJwgOKCbx5zZDcx7GJPpEeIXx437I7i_7OHK6Y0WzzGTbKoo9-xNIQ8tmvefO80DuPCrWOycHzYPqM3lCxYd5nFJmetqpS1VChmhuGBdDQ7aatPjHae8Wxqj8CEAbHb7rMv6abVlPTsLdBSYaM4Ga58qxlgN', access_token='BQDzA1ioKqzQWwdnaqNcPyePPF7wNdEohRx1DupaOfEJHwHlL-M1q5kYo5WwgGRrlp-lBHTNxGhKz7X2MwVbShfUQtAf4bQW3qc1OsHS24S6kzHIh1-v4q1XeCrl_wjyE2PeVjJ_8JNHHrzakwaXq0NmW9NVFlHXG8hE4-3twjprw4CU5oElIZGAXroN', refresh_token='AQB9pDCl6Ttj309il_fnfHW5TDml-w9iBvrK-ca24ZGt0XrxKFqqDgEX6XoNCYX5tj-MFehlekmAjCtHONJuiLVlN1DkJAvK7kV7n5HKXQgFQa-yd0jAdooX0_400me9bsw', user_id=None, display_name=None, token_expiration_time=1642214357)
    asyncio.run(async_get(me))


async def async_get(user):
    session = aiohttp.ClientSession()
    await user_apis.get_profile(session, user)
    playlist_list = await playlist_apis.get_current_users_playlists(session, user)