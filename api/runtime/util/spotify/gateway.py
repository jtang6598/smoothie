import json
from python_settings import settings

async def spotify_get(session, api, params=None, body=None, headers=None, auth=None, isjson=True, base_url=settings.SPOTIFY_WEB_API):
    if isjson and body:
        body = json.dumps(body)
    async with session.get(base_url + api, params=params, data=body, headers=headers, auth=auth) as response:
        response.raise_for_status()
        response_json = json.loads(await response.text())
        return response_json

async def spotify_post(session, api, params=None, body=None, headers=None, auth=None, isjson=True, base_url=settings.SPOTIFY_WEB_API):
    if isjson and body:
        body = json.dumps(body)
    async with session.post(base_url + api, params=params, data=body, headers=headers, auth=auth) as response:
        response.raise_for_status()
        response_json = json.loads(await response.text())
        return response_json

    