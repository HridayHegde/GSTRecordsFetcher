import requests
import autentication
import os 
from datetime import datetime
import csv
import json

from config import config


baseurl = "https://api.quicko.com/gsp/public/gstr?"


def getgstdata(gstdatalist):
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

    authtoken = autentication.authenticate()

    for x in gstdatalist:
        temp_gstn = x[0]
        temp_fy = x[1]
        url = baseurl+"gstin="+temp_gstn+"&"+"financial_year="+temp_fy
        print(url)
        headers = {'Authorization': authtoken, 
            'x-api-key': config.api_key,
            'x-api-version': '3.3'
        }
        response = requests.request("GET", url, headers=headers)
        print(response.text)
        jsondata = json.loads(response.text)
        
        if not jsondata["code"]:
            for x in jsondata['data']:
                writetocsv(x,dt_string)
        else:
            print("API ERROR")

        writeblanklinetocsv(dt_string)





        

def writetocsv(datadict,dt_string):
    fileexists = os.path.isfile("/Output"+"/Generated"+dt_string+"_DATA.csv")
    csv_file = open("/Output"+"/Generated"+dt_string+"_DATA.csv",mode='a')


    writer = csv.DictWriter(csv_file,datadict.keys())
    if not fileexists:
        writer.writeheader()
        
    return fileexists



def writeblanklinetocsv(dt_string):
    fileexists = os.path.isfile("/Output"+"/Generated"+dt_string+"_DATA.csv")
    if fileexists:
        csv_file = open("/Output"+"/Generated"+dt_string+"_DATA.csv",mode='a',newline='\n')
        writer = csv.DictWriter(csv_file)
        writer.writerow()
    else:
        print("File Does Not Exist")

#getgstdata([['27AAACT3151E1ZP','fy 2017-18']])

