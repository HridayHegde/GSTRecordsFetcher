import json
import requests
from config import config

url = "https://api.quicko.com/authenticate"

api_key = config.api_key
api_secret = config.api_secret

headers = {
  'x-api-key': api_key,
  'x-api-secret': api_secret,
  'x-api-version': '3.3'
}

def authenticate():
  
  response = requests.request("POST", url, headers=headers)
  
  #print(response.text)
  data = json.loads(response.text)

  accesstoken = data["access_token"]


  return accesstoken


    