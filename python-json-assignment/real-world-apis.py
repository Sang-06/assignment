import json

api_response = '''
{
    "status": "success",
    "data": {
        "user": {
            "id": 101,
            "profile": {
                "name": "Alice",
                "age": 30,
                "email": "alice@example.com"
            }
        }
    }
}
'''

data = json.loads(api_response)

print("User Name:", data["data"]["user"]["profile"]["name"])