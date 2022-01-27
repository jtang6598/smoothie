import string
import secrets
from util.dao.GroupsDAO import GroupsDao
from util.auth.AuthorizationHandler import AuthorizationHandler
import util.utils as utils

# Create a group and return the group id to the client
async def main(event, context):
    # TODO: input sanitization
    code = event['code']
    redirect_uri = event['redirect_uri']
    
    client_session = await utils.get_client_session()
    # response = await AuthorizationHandler.request_access_token(client_session, code, redirect_uri)
    # access_token = response['access_token']
    # refresh_token = response['refresh_token']
    
    access_token = "dummy access"
    refresh_token = "dummy response"

    alphabet = string.ascii_letters + string.digits
    group_id = ''.join(secrets.choice(alphabet) for i in range(8))

    dao = GroupsDao()
    dao.put_group(group_id, access_token, refresh_token)

    body = {"id": group_id}

    await client_session.close()

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
