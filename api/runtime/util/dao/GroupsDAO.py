import boto3
from boto3.dynamodb.conditions import Key
from python_settings import settings

class GroupsDao:
    def __init__(self):
        self._dynamodb = boto3.resource('dynamodb')
        self._table = self._dynamodb.Table(settings.GROUPS_TABLE)
  
    def put_group(self, id: str, access_token: str, refresh_token: str) -> None:
        item = {
            "id": id,
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        self._table.put_item(Item=item)
    
    def group_exists(self, id: str) -> bool:
        response = self._table.query(KeyConditionExpression=Key("id").eq(id))
        items = response["Items"]
        return len(items) > 0