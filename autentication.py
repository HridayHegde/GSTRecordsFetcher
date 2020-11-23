import json
import requests
from config import config

url = "https://api.quicko.com/authenticate"

api_key = config.getapi_key()
api_secret = config.getapi_secret()

print(api_key)
print(api_secret)
headers = {
  'x-api-key': api_key,
  'x-api-secret': api_secret,
  'x-api-version': '3.3'
}

def authenticate():
  
  try:  
    response = requests.request("POST", url, headers=headers)
  except OSError as e:
    print(e)
  #print(response.text)
  data = json.loads(response.text)

  print(data)
  accesstoken = data["access_token"]


  return accesstoken


    