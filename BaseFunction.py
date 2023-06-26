import json
from colorama import Fore, Back, Style
from datetime import datetime
import sys
import os
from os import system, name
from time import sleep
import shutil


def clearScreen():
    # for windows
    if name == 'nt':
        _ = system('cls')
        print("ted")
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


## Load Json File and return it as Dictionary
def LoadJsonFile(JsonFile): 
   try:
     JsFile = open(JsonFile, "r")
     js = JsFile.read()
   except:
     print(Style.BRIGHT + Fore.RED + "Json File Not Found [ " + Fore.WHITE + JsonFile + Fore.RED + " ] " + Style.RESET_ALL)  
     sys.exit()
   finally:
      JsFile.close()            

   
   js  = js.replace('\n', '') 
   global JsonConfig   
   return json.loads(js)


def CheckExistDir(Path,Title,PrintIt = True):
  if os.path.exists(Path) is False:
    if PrintIt is True:       
       print(Style.BRIGHT + Fore.WHITE +  Title + " [ " + Style.BRIGHT + Fore.LIGHTRED_EX + Path + Fore.WHITE + Style.BRIGHT +" ] not exists " + Style.RESET_ALL)                     
       print(Style.BRIGHT + Fore.WHITE + "If the path is correct, for create run this Comand [ " + Fore.CYAN + "mkdir -p {}".format(Path) + Fore.WHITE + " ] " + Style.RESET_ALL )         
    return False  
  else:
    return True

def CheckExistFile(Path,Title,PrintIt = True):
  if os.path.exists(Path) is True:
    return True
  else:
    if PrintIt is True:       
       print(Style.BRIGHT + Fore.WHITE + Title + "File [ " + Style.BRIGHT + Fore.LIGHTRED_EX + Path + Fore.WHITE + Style.BRIGHT +" ] Not found " + Style.RESET_ALL)                        
    return False

def CheckExist(path,FileOrDir, title,Verbus):  
  if os.path.exists(path) is True:
    return True
  else:
    if FileOrDir.lower() == "file":
       if Verbus is True:
          print(Style.BRIGHT + Fore.WHITE + title + "File [ " + Style.BRIGHT + Fore.LIGHTRED_EX + path + Fore.WHITE + Style.BRIGHT +" ] Not found " + Style.RESET_ALL)                        
       return False
    elif FileOrDir.lower() == "folder":
       if Verbus is True:
          print(Style.BRIGHT + Fore.WHITE +  title + " [ " + Style.BRIGHT + Fore.LIGHTRED_EX + path + Fore.WHITE + Style.BRIGHT +" ] not exists " + Style.RESET_ALL)                     
       return False
    elif FileOrDir.lower() == "dir":
       if Verbus is True:       
          print(Style.BRIGHT + Fore.WHITE +  title + " [ " + Style.BRIGHT + Fore.LIGHTRED_EX + path + Fore.WHITE + Style.BRIGHT +" ] not exists " + Style.RESET_ALL)                     
          print(Style.BRIGHT + Fore.WHITE + "If the path is correct, for create run this Comand [ " + Fore.CYAN + "mkdir -p {}".format(path) + Fore.WHITE + " ] " + Style.RESET_ALL )
       return False

def GetValue(InputDict,Key):  
  try:
    Value = InputDict[Key]        
  except:    
    print(Style.BRIGHT + Back.RED+ Fore.WHITE + "Value (({})) Not Found / GetValue Function in BaseFunction.py".format(Key) + Style.RESET_ALL)
    input(Style.BRIGHT + Fore.WHITE + "Press Any Key to ... ")
    return None    
  
  return Value

def GetJsonObject(InputJsonConfig,jsonkey,ObjectType):      
  try:
    a = InputJsonConfig[jsonkey]
    if ObjectType == "str":
       ReturnObj = ""
       ReturnObj = a
       return ReturnObj
    elif ObjectType == "list":
      Returnlist = []
      Returnlist = list(a)
      return Returnlist
    elif ObjectType == "dic":
      Returndic = {} 
      Returndic = a.copy()     
      return Returndic    
    elif ObjectType == "bool":
      Returndic = False
      Returndic = a
      return Returndic        
    else:
      print("ObjectTypeInvalid In FnGetJsonObject()")
    
  except KeyError:    
    if ObjectType == "str":
      ReturnObj = ""      
      return ReturnObj
    elif ObjectType == "list":
      Returnlist = []
      return Returnlist
    elif ObjectType == "dic":
      Returndic = {}      
      return Returndic
    else:
      print("ObjectTypeInvalid In FnGetJsonObject()")
  

def logit(LogFileName,action,message):
    #LogFileName = JsonConfig["LogPath"] +"/BackupWP-"+ Now + ".logs"
    try:
      f = open(LogFileName, "a")
      try:
        DateAndTime = datetime.now()
        DateAndTime = DateAndTime.strftime("%d/%m/%Y %H:%M:%S")
        logs = "\n[ {:^20} ] - [ {:^20} ] - [ {:<50} ]"        
        f.write(logs.format(DateAndTime, action, message ))        
      except:
        print("Something went wrong when writing to the log file [ " + Fore.RED + LogFileName + Fore.RESET + " ]")
      finally:
        f.close()
    except:
      print("Something went wrong when writing to the log file [ " + Style.BRIGHT +  Fore.RED + LogFileName + Style.RESET_ALL + " ]")

def ChekSizeFile(FileName,WaitTime):    
    FileStats = os.stat(FileName)
    FileSize1 = FileStats.st_size
    sleep(WaitTime)
    FileStats = os.stat(FileName)
    FileSize2 = FileStats.st_size
    if FileSize1 == FileSize2:
       return True
    else:
       return False

def DeleteFileOrDir(path,verbus = True):  
  Resualt = ""
  if os.path.exists(path):
    if os.path.isfile(path):       
       try:
         os.remove(path)         
         if verbus is True:
            print(Fore.WHITE + Style.BRIGHT + "Remove file [ " + Fore.RED + path + Fore.WHITE +" ]" + Style.RESET_ALL)
         return [True,""]       
       except FileNotFoundError:
         if verbus is True:
            print(Fore.RED + Style.BRIGHT + "File not found [ " + Fore.WHITE + path + Fore.RED + " ]" + Style.RESET_ALL )         
         return [False,"File not found"]
       except PermissionError:
         if verbus is True:
            print(Fore.RED + Style.BRIGHT + "Permission denied for Delete file [ " + Fore.WHITE + path + Fore.RED + " ]" + Style.RESET_ALL)
         return [False,"Permission denied for Delete file"]
       except:
         if verbus is True:
            print("Something went wrong to Delele file [{}]".format(path))                  
         return [False,"Something went wrong to Delele file"]                                                             
    elif os.path.isdir(path):       
       try:
         shutil.rmtree(path)
         if verbus is True:
            print(Fore.WHITE + Style.BRIGHT + "Remove Direcory [ " + Fore.RED + path + Fore.WHITE +" ]" + Style.RESET_ALL)                
         return [True,""]         
       except FileNotFoundError:
         if verbus is True:
            print("Directory not found [{}]".format(path))
         return [False,"Directory not found"]
       except PermissionError:         
         if verbus is True:
            print(Fore.RED + Style.BRIGHT + "Permission denied for Delete file [ " + Fore.WHITE + path + Fore.RED + " ]" + Style.RESET_ALL)         
         return [False,"Permission denied for Delete file"]
       except:         
         if verbus is True:
            print("Something went wrong to Delele Directory [{}]".format(path))         
         return [False,"Something went wrong to Delele Directory"]
  else:
    if verbus is True:
        print("File or directory [ {} ] Not Found".format(path))
    return [False,"File or directory nof found"]

def CheckErrorNumScp(ErrorNo):
   if ErrorNo == 0:
      return ""
   elif ErrorNo == 256:
      return "File or Directory Not Found"
   else:
      return "Unknow Error"
      
def Now(FormatType = "full"):
  Now = datetime.now()  
  if FormatType == "full":
     Now = Now.strftime("%Y-%m-%d_%H-%M-%S")
  elif FormatType == "time":
     Now = Now.strftime("%H-%M-%S")
  elif FormatType == "date":
     Now = Now.strftime("%Y-%m-%d")
  elif FormatType == "view":
     Now = Now.strftime("%Y/%m/%d %H:%M:%S")
     
  return Now



def WriteJsonFile(JsonFile,Dict,overwrite = True):    
    try:
        if overwrite:
           lsfile = open(JsonFile, "w")          
        else:
           lsfile = open(JsonFile, "a")
        try:
            lsfile.write(json.dumps(Dict, indent=4))            
            WriteStatus = True
        except:
            print("Something went wrong when writing to the file")    
            WriteStatus = False
        finally:
            lsfile.close()
    except:
      print("Something went wrong when writing to the file")      
      WriteStatus = False
    finally:          
        lsfile.close()            
    if WriteStatus:
       return True
    else:
       return False
       
       

