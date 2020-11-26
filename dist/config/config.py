import json

def getapi_key():
    configfile = open("./config/config.json")
    jsondata = json.load(configfile)

    return jsondata["api_key"]

def getapi_secret():
    configfile = open("./config/config.json")
    jsondata = json.load(configfile)
    return jsondata["api_secret"]





