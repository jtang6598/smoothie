def main(event, context):
  return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "createPlaylist succeeded"
    }