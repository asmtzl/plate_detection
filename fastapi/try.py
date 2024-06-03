import requests
import json
url = "https://eu-central-1.aws.data.mongodb-api.com/app/data-wkjrwcs/endpoint/data/v1/action/findOne"

payload = json.dumps({
    "collection": "user",
    "database": "plateUsers",
    "dataSource": "plateDet",
    "projection": {
        "_id": 1,
        "name": 2,
        "username":3
        
    }
})
headers = {
  'Content-Type': 'application/json',
  'Access-Control-Request-Headers': '*',
  'api-key': 'KHmaotDECE6YJJnArAG9c8obaNf9d4p372YWx667ICfbXONTZXHgHnCL6SmXzj2G',
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
