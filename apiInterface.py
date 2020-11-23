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
            'x-api-key': config.getapi_key(),
            'x-api-version': '3.3'
        }
        try: 
            response = requests.request("GET", url, headers=headers)
        except OSError as e:
            print(e)
            print("API ERROR")
        #print(response.text)

        jsondata = json.loads(response.text)
        
        

        if not "code" in jsondata:
            headerlist = ["GST Number"]
            
            for items in list(jsondata[0].keys()):
                    print(items)
                    headerlist.append(items)

            print(headerlist)
            for data in jsondata:
                writedict  = {"GST Number" : temp_gstn}
                writedict.update(data)
                print(writedict)
                writetocsv(headerlist,writedict,dt_string)

            writeblanklinetocsv(headerlist,dt_string)

        else:
            print("API ERROR")
            print(jsondata)
        

        




        

def writetocsv(headerlist,datadict,dt_string):
    fileexists = os.path.isfile("./Output"+"/Generated"+dt_string+"_DATA.csv")
    csv_file = open("./Output"+"/Generated"+dt_string+"_DATA.csv",mode='a')

    writer = csv.DictWriter(csv_file,fieldnames = headerlist)
    if not fileexists:
        print(fileexists)
        writer.writeheader()

    writer.writerow(datadict)    
    return fileexists



def writeblanklinetocsv(headerlist,dt_string):
    fileexists = os.path.isfile("./Output"+"/Generated"+dt_string+"_DATA.csv")
    if fileexists:
        csv_file = open("./Output"+"/Generated"+dt_string+"_DATA.csv",mode='a')
        writer = csv.DictWriter(csv_file,fieldnames = headerlist)
        writer.writerow({})
    else:
        print("File Does Not Exist")

#getgstdata([['27AAACT3151E1ZP','FY 2017-18'],['27AAACK4409J1ZK','FY 2017-18']])

