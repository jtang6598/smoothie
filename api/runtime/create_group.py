import asyncio
import botocore.exceptions
import string
import secrets

from util.dao.GroupsDAO import GroupsDao
from util.auth.AuthorizationHandler import AuthorizationHandler
import util.utils as utils

# Create a group and return the group id to the client
def main(event, context):
    # TODO: input sanitization
    statusCode = 200
    code = event['code']
    redirect_uri = event['redirect_uri']
    
    client_session = asyncio.run(utils.get_client_session())
    # TODO: wrap in try catch
    response = AuthorizationHandler.request_access_token(client_session, code, redirect_uri)
    if 'accest_token' or 'refresh_token' not in response:
        statusCode = 400
        body = {"error": "Invalid login credntials"}
    else:
        access_token = response['access_token']
        refresh_token = response['refresh_token']

        alphabet = string.ascii_letters + string.digits
        group_id = ''.join(secrets.choice(alphabet) for i in range(8))

        try:
            dao = GroupsDao()
            dao.put_group(group_id, access_token, refresh_token)
        except botocore.exceptions.ClientError as error:
            statusCode = 500
            body = {"error": "Unable to create group"}
            print(error.response)
        else:
            body = {"id": group_id}

    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
