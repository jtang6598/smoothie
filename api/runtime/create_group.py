import aiohttp
import asyncio
from smoothie.data_objects.User import User
from smoothie.auth.AuthorizationHandler import AuthorizationHandler

# wip
def main(event, context):
    code = event['code']
    user = User(code=code)
    
    client_session = aiohttp.ClientSession()
    auth_handler = AuthorizationHandler(client_session)
    response = asyncio.run(auth_handler.request_access_token(user))

    print(response)

    client_session.close()

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "createGroup succeeded"
    }

if __name__ == "__main__":
    event = {"code": "dummy code"}
    main(event, None)
