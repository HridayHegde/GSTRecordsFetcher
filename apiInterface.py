import requests
import autentication
import os 
from datetime import datetime
import csv
import json
import pandas as pd

from config import config
#import pandasModel

#import pandas as pd

baseurl = "https://api.quicko.com/gsp/public/gstr?"

global df
df = None
def getgstdata(gstdatalist):
    dataconfigfile = open("./config/dataconfig.json")
    configjsondata = json.load(dataconfigfile)
    global df
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    status = False
    authtoken = autentication.authenticate()
    jsondata = None
    if not authtoken == "Null":
        for x in gstdatalist:
            message = "Unknown Error"
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
                headerlist = ["GST Number","Financial Year"]
                
                for items in configjsondata["fields"]:
                        print(items)
                        headerlist.append(items)
                if not isinstance(df,pd.DataFrame):
                    df = pd.DataFrame(columns=headerlist)
                print(headerlist)
                for data in jsondata:
                    tempdata ={}
                    for field in configjsondata["fields"]:
                        if not field == "ret_prd":
                            tempdata[field] = data[field]
                        else:
                            changeddata = ""
                            retperioddata = data["ret_prd"]
                            changeddata = datetime.strptime(retperioddata, "%m%Y").strftime("%b-%Y")
                            tempdata[field] = changeddata
                    writedict  = {"GST Number" : temp_gstn,"Financial Year": temp_fy}
                    #print(data)
                    
                    writedict.update(tempdata)
                    df = df.append(writedict, ignore_index=True)
                    print(writedict)
                    #writetocsv(headerlist,writedict,dt_string)
                
                
                status = True
                #writeblanklinetocsv(headerlist,dt_string)

            else:
                print("API ERROR")
                status = False
                print(jsondata)
                message = jsondata["message"]
        writedftocsv(df,dt_string)
                
        return status,message
    else:
        if not jsondata == None: 
            if "message" in jsondata:
                return False,jsondata["message"]
            else:
                return False,"Unknow Error"
        else:
            return False,"API Data Not Recieved"

def writedftocsv(df,dt_string):
    fileexists = os.path.isfile("./Output"+"/Generated"+dt_string+"_DATA.csv")
    if not fileexists:
        df.to_csv("./Output"+"/Generated"+dt_string+"_DATA.csv",mode='a',index=False)
        

def writetocsv(headerlist,datadict,dt_string):
    fileexists = os.path.isfile("./Output"+"/Generated"+dt_string+"_DATA.csv")
    csv_file = open("./Output"+"/Generated"+dt_string+"_DATA.csv",mode='a',newline='')

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

