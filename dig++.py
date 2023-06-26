#! /usr/bin/python3
import BaseFunction as base
from colorama import Fore, Back, Style
import sys
import signal
import requests
import os
from os import system, name
import subprocess

ConfigFile = "/home/beigi/myAplication/DNS++/config/config.json"
SrverlistFile = "/home/beigi/myAplication/DNS++/config/serverList.json"

if base.CheckExistFile(ConfigFile,"config.json") is False:
    sys.exit()
JsonConfig = base.LoadJsonFile(ConfigFile)

if base.CheckExistFile(SrverlistFile,"Serverlist.json") is False:
    sys.exit()
JsonServerList = base.LoadJsonFile(SrverlistFile)

EnableWriteJsonServerFile = False
EnableDnsSearch = False
################################################
################################################

def handler(signum, frame):
    print("")
    print("")
    print(Style.NORMAL + Fore.RED + " Force Exit By press [ " + Fore.WHITE + "CTRL + C" + Fore.RED + " ]")
    print("")
    sys.exit()

def FnExit():
    print (Style.NORMAL + Fore.WHITE + "Bye :)")
    sys.exit()
    
def FnChOS():
    # for windows
    if name == 'nt':        
        msg = """
This progarm Use ( {dig} ) command, this commad by default Avalable on linux.,
If you want to run this program in Windows, you need to install {bind} software to add the {dig} command to the operating system
For more information, see the link below ,

{url}
""".format(dig = Fore.RED + "dig" + Fore.WHITE, bind = Fore.GREEN + "bind" + Fore.WHITE, url = Fore.BLUE + "https://phoenixnap.com/kb/dig-windows" + Fore.WHITE)
        print(Style.BRIGHT + Fore.WHITE + msg)
        FnExit()
    

def PrintBanner():
    print (Style.BRIGHT + "")
    print (Fore.CYAN + "  ____      ____  _   _______    ________              __                ____   " )
    print (Fore.CYAN + " / / /     / __ \/ | / / ___/   / ____/ /_  ___  _____/ /_____  _____    \ \ \  " )
    print (Fore.CYAN + "/ / /     / / / /  |/ /\__ \   / /   / __ \/ _ \/ ___/ //_/ _ \/ ___/     \ \ \ " + Style.NORMAL )
    print (Fore.CYAN + "\ \ \    / /_/ / /|  /___/ /  / /___/ / / /  __/ /__/ ,< /  __/ /         / / / " )
    print (Fore.CYAN + " \_\_\  /_____/_/ |_//____/   \____/_/ /_/\___/\___/_/|_|\___/_/         /_/_/  " )
    print (Style.RESET_ALL + "                                                                                " )


def PrintGlobalStatus():
    TotalNumber = 0
    ActiveNumber = 0
    global EnableDnsSearch
    
    for x in JsonServerList:
        TotalNumber += 1
        ServerInfo = base.GetValue(JsonServerList,x)                    
        if ServerInfo["Enable"] is True:
            ActiveNumber += 1            

    if TotalNumber == 0:
        print(Style.BRIGHT + Fore.RED + "No Server Found, Please check (ServerList.json) file" + Style.RESET_ALL)
        FnExit()

    print(Style.NORMAL + Fore.WHITE + "Total DNS Server Number  : " + Fore.BLUE + str(TotalNumber) + Style.RESET_ALL)
    print(Style.NORMAL + Fore.WHITE + "Active DNS Server Number : " + Fore.YELLOW + str(ActiveNumber) + Style.RESET_ALL)
    print(Style.NORMAL + Fore.WHITE + "Last Update              : " + Fore.YELLOW + JsonConfig["LastUpdate"]+Style.RESET_ALL)    
    if ActiveNumber == 0 :        
        EnableDnsSearch = False
        return False            
    else:
        EnableDnsSearch = True
        return True


        
def PrinitMainMenu():
    print("")
    print(Style.NORMAL + Fore.WHITE + "Type {}, for Help".format(Fore.LIGHTBLUE_EX + "h" + Fore.WHITE) )
    print(Style.NORMAL + Fore.WHITE + "Type {}, for quit".format(Fore.LIGHTBLUE_EX + "q" + Fore.WHITE) )
    print(Style.NORMAL + Fore.WHITE + "Type {}, for Get Local DNS".format(Fore.LIGHTBLUE_EX + "l" + Fore.WHITE) )
    print(Style.NORMAL + Fore.WHITE + "Type {}, for List all Servers ".format(Fore.LIGHTBLUE_EX + "all" + Fore.WHITE) )    
    print(Style.NORMAL + Fore.WHITE + "Type {}, or press {} for List all active Servers ".format(Fore.YELLOW + "Active" + Fore.WHITE,Fore.YELLOW + "Enter" + Fore.WHITE))
    print(Style.NORMAL + Fore.WHITE + "Type {}, check status of Servers  ".format(Fore.GREEN + "check" + Fore.WHITE) )
    if EnableWriteJsonServerFile:
        print(Style.NORMAL + Fore.WHITE + "Type {}, for update Json Servelist File  ".format(Fore.RED + "update" + Fore.WHITE) )    
    if EnableDnsSearch is True:
        UserInpt = input(Style.NORMAL + Fore.WHITE + "Type This {PAR} or type {DNS} for DNS check :".format(PAR = Fore.LIGHTBLUE_EX + "Parameter"+ Fore.WHITE,DNS = Fore.LIGHTBLUE_EX + "DNS" + Fore.WHITE))
    else:
        print("")
        print(Style.BRIGHT + Fore.WHITE + "No active servers found. You can check the status of the servers and find the active servers by typing {}".format(Fore.RED + "check" + Fore.WHITE))
        UserInpt = input(Style.NORMAL + Fore.WHITE + "Type {PAR} :".format(PAR = Fore.LIGHTBLUE_EX + "Parameter" + Fore.WHITE))                
    if UserInpt.lower() == "":
        UserInpt = "active"

    if UserInpt.lower() == "q":
        FnExit()
    elif UserInpt.lower() == "h":
        PrintHelp()
    elif UserInpt.lower() == "l":
        fnLocalDig()
    elif UserInpt.lower() == "all":
        base.clearScreen()
        PrintBanner()
        PrintGlobalStatus()               
        PrintListofAllServer()
        PrinitMainMenu()
    elif UserInpt.lower() == "active":
        base.clearScreen()
        PrintBanner()
        PrintGlobalStatus()               
        PrintListofActiveServer()
        PrinitMainMenu()        
    elif UserInpt.lower() == "check":    
        FnRestJsonListStatus()
        FnCheckServers()        
    elif UserInpt.lower() == "update":
        if EnableWriteJsonServerFile:
            base.clearScreen()  
            PrintBanner()
            PrintGlobalStatus()
            WriteServerList()
            PrinitMainMenu()
        else:
            base.clearScreen()
            PrintBanner()        
            print("")
            print(Style.BRIGHT + Fore.WHITE + "((Parameter [ {} ] not valid))".format(Fore.RED + UserInpt + Fore.WHITE))
            PrinitMainMenu()
    else:
        if EnableDnsSearch is False:
            base.clearScreen()
            PrintBanner()        
            print("")
            print(Style.BRIGHT + Fore.WHITE + "((Parameter [ {} ] not valid))".format(Fore.RED + UserInpt + Fore.WHITE))
            PrinitMainMenu()
        else:
            base.clearScreen()
            PrintBanner()
            PrintGlobalStatus()
            global activeList
            activeList = GetDictofActiveServer()
            FnCheckDNS(UserInpt)            
            

def FnCheckDNS(Input):
    for ID in activeList:
        server = base.GetValue(activeList,ID)
        ip = (server["IP"])
        returned = fnDig(ip,Input)
        if returned != "":
            returned = returned.strip()
            returned = returned.replace('\n',' ')
            dnslist = []
            dnslist = list(returned.split(" "))
            #dnslist.append(returned)
            activeList[ID]["DNS"] = dnslist         
        base.clearScreen()
        PrintBanner()
        PrintGlobalStatus()
        printResualDNSSearch()        
    PrinitMainMenu()            

def printResualDNSSearch():
    for x in activeList:
        ServerInfo = base.GetValue(activeList,x)        
        Xstate = Fore.CYAN + base.GetValue(ServerInfo,"City/Stat") + Fore.WHITE
        XCountry = Fore.LIGHTCYAN_EX + base.GetValue(ServerInfo,"Country") + Fore.WHITE
        XCompany = base.GetValue(ServerInfo,"Company")
        XDNs = Fore.YELLOW + str(base.GetValue(ServerInfo,"DNS")) + Fore.WHITE
        print (Fore.WHITE + "{:<80}{:<20}".format(XCompany +", "+ Xstate + ", " + XCountry,XDNs))
        


def FnRestJsonListStatus():
    for ID in JsonServerList:    
        server = base.GetValue(JsonServerList,ID)
        JsonServerList[ID]["Enable"] = False

def FnCheckServers():
    global EnableWriteJsonServerFile 
    EnableWriteJsonServerFile = True    
    for ID in JsonServerList:
        server = base.GetValue(JsonServerList,ID)
        ip = (server["IP"])
        returned = fnDig(ip,"www.google.com")
        if returned != "":
            Status = Fore.GREEN + "Active" + Fore.WHITE
            JsonServerList[ID]["Enable"] = True            
        else:
            Status = Fore.RED + "Deactive" + Fore.WHITE
            JsonServerList[ID]["Enable"] = False        
        base.clearScreen()
        PrintBanner()
        PrintGlobalStatus()               
        PrintListofAllServer()
    WriteServerList()        
    PrinitMainMenu()        


def WriteServerList():
    global EnableWriteJsonServerFile
    EnableWriteJsonServerFile = True
    print ("")
    UserInput = input(Style.NORMAL + Fore.WHITE + "do you want update Servers Status in file [ {} ] Y/n: ?".format(Fore.BLUE + "serverList.json" + Fore.WHITE))
    if UserInput == "":
        UserInput = "y"
    if UserInput.lower() == "y":
       if base.WriteJsonFile(SrverlistFile,JsonServerList):       
           print("")
           print(Style.BRIGHT + Fore.GREEN + "      ((JSON ServerList Updated ))" + Style.RESET_ALL)
           EnableWriteJsonServerFile = False
           print("")
       else:
           print("")
           print(Style.BRIGHT + Fore.RED + "      ((JSON ServerList Updated Failed))" + Style.RESET_ALL)    
           print("")
    #JsonServerList["ID"]["Enable"] = False               
    JsonConfig["LastUpdate"] = base.Now("view")
    base.WriteJsonFile(ConfigFile,JsonConfig)


def fnLocalDig():
    base.clearScreen()
    PrintBanner()
    print("")
    print(Style.NORMAL + Fore.WHITE + "Local DNS Active !" + Style.RESET_ALL)
    UserInput = input(Style.NORMAL + Fore.WHITE + "Type [ {DNS} ] or type [ {ENTER} ] for Back to Main Menu : ".format(DNS = Fore.YELLOW + "DNS" + Fore.WHITE, ENTER = Fore.RED + "Enter" + Fore.WHITE) )
    if UserInput == "":
        START()
    else:    
        Command = "dig {xSite} +short".format(xSite = UserInput )    
        CommandList = Command.split(" ")        
        try:
            returned_output = subprocess.check_output(CommandList)
            returnedstr = returned_output.decode("utf-8")        
        except:
            returnedstr = ""

    returnedstr = returnedstr.strip()
    returnedstr = returnedstr.replace('\n',' ')
    LocaDnslist = []                          
    LocaDnslist = list(returnedstr.split(" "))
    print ("")        
    print (Style.NORMAL + Fore.WHITE + "(( Local DNS is {} ))".format(Fore.YELLOW + str(LocaDnslist) + Fore.WHITE ))
    print ("")        
    PrinitMainMenu()
    
        
def fnDig(DNS,Site):
    Command = "dig @{xDNS} {xSite} +short".format(xDNS = DNS, xSite = Site )    
    CommandList = Command.split(" ")    
    #Resulst = os.system(Command)
    try:
        returned_output = subprocess.check_output(CommandList)
        returnedstr = returned_output.decode("utf-8")
        return returnedstr
    except:
        return ""

def GetDictofActiveServer():
    returnit = {}
    ID = 1
    for x in JsonServerList:
        serverInfo = base.GetValue(JsonServerList,x)                
        serverInfo.update({"DNS":[]})
        if serverInfo["Enable"]:           
           returnit.update({"DNSID-"+str(ID):serverInfo})           
           ID += 1
    return returnit       

def PrintListofActiveServer():
    print("")
    CountOfServer = 0    
    for ID in JsonServerList:
        xServer = base.GetValue(JsonServerList,ID)
        if base.GetValue(xServer,"Enable"):
            Xstatus = Fore.YELLOW+"Active"+Fore.WHITE            
            Xstate = Fore.CYAN + base.GetValue(xServer,"City/Stat") + Fore.WHITE
            XCountry = Fore.LIGHTCYAN_EX + base.GetValue(xServer,"Country") + Fore.WHITE
            XCompany = base.GetValue(xServer,"Company")                       
            print (Fore.WHITE + "{:<80}{:<20}".format(XCompany +", "+ Xstate + ", " + XCountry,Xstatus))
            CountOfServer += 1
    if CountOfServer == 0:
            print("")
            print(Style.BRIGHT + Fore.CYAN + "      (( No Active Server Found ))" + Style.RESET_ALL) 
            print("")

def PrintListofAllServer():
    print("")    
    for ID in JsonServerList:
        xServer = base.GetValue(JsonServerList,ID)
        Xstate = Fore.CYAN + base.GetValue(xServer,"City/Stat") + Fore.WHITE
        XCountry = Fore.LIGHTCYAN_EX + base.GetValue(xServer,"Country") + Fore.WHITE
        XCompany = base.GetValue(xServer,"Company")
        if base.GetValue(xServer,"Enable"):
            Xstatus = Fore.YELLOW+"Active"+Fore.WHITE
        else:    
            Xstatus = Fore.RED+"DeActive"+Fore.WHITE
        print (Fore.WHITE + "{:<80}{:<20}".format(XCompany +", "+ Xstate + ", " + XCountry,Xstatus))
        
 
def PrintHelp():
    print("Help")

def START():
    base.clearScreen()
    PrintBanner()    
    PrintGlobalStatus()
    PrinitMainMenu()



#################################################
#################################################

signal.signal(signal.SIGINT, handler)


FnChOS() # Check OS
START()


