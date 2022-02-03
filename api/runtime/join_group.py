import asyncio
import botocore.exceptions
from util.dao.GroupsDAO import GroupsDao
from util.auth.AuthorizationHandler import AuthorizationHandler
import util.utils as utils

def main(event, context):
    # Validate that the group exists
    statusCode = 200
    body = {}
    group_id = event["id"]
    group_dao = GroupsDao()
    group_exists = group_dao.group_exists(group_id)
    print(f"id={group_id}, group_exists={group_exists}")

    if group_exists:
        # Get credentials if the group exists
        code = event['code']
        redirect_uri = event['redirect_uri']
        client_session = asyncio.run(utils.get_client_session())
        response = AuthorizationHandler.request_access_token(client_session, code, redirect_uri)
        if 'accest_token' or 'refresh_token' not in response:
            statusCode = 400
            body = {"error": "Invalid login credntials"}
        else:
            # Save the credentials
            access_token = response['access_token']
            refresh_token = response['refresh_token']
            try:
                group_dao.put_group(group_id, access_token, refresh_token)
            except botocore.exceptions.ClientError as error:
                statusCode = 500
                body = {"error": "Unable to create group"}
                print(error.response)
            else:
                statusCode = 200
                body = {"id": group_id}
    else:
        statusCode = 400
        body = {"error": "Invalid group id"}
    
    return {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }