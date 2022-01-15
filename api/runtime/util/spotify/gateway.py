import json

async def spotify_get(session, url, params=None, body=None, headers=None, auth=None):
    async with session.get(url, params=params, data=body, headers=headers, auth=auth) as response:
        response.raise_for_status()
        response = json.loads(await response.text())
        return response

async def spotify_post(session, url, params=None, body=None, headers=None, auth=None):
    async with session.post(url, params=params, data=body, headers=headers, auth=auth) as response:
        response.raise_for_status()
        response = json.loads(await response.text())
        return response

