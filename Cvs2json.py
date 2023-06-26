#! /usr/bin/python3
import re
import json

serverDic = {}
JsonFile = "/home/beigi/myAplication/DNS++/config/serverList.json"

File = open("/home/beigi/myAplication/DNS++/config/dnslist.txt","rt")
ID = 1
for x in File:
    tmplist1 = []
    tmplist = []
    if re.findall("\A#", x):
        pass
    else:       
        x = x.rstrip()
        tmplist = x.split(",")
        Xcity, xCuntry, Xcompany, Xip = tmplist
        tmpdic = {"City/Stat": Xcity.strip(), "Country": xCuntry.strip(), "Company":Xcompany.strip(), "IP":Xip.strip(),"Enable":False}
        #serverDic.update({sCode: tmpdic})
        serverDic.update({"DNSID-"+str(ID):tmpdic})
        ID += 1



def CreateJson():
    try:
        lsfile = open(JsonFile, "w")
        try:
            lsfile.write(json.dumps(serverDic, indent=4))
        except:
            print("Something went wrong when writing to the file")    
        finally:
            lsfile.close()
    except:
      print("Something went wrong when writing to the file")    


CreateJson()