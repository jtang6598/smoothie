import boto3
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