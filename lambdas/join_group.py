"""Testing, empty commit"""
def main(event, context):
  return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": "joinGroup succeeded"
    }