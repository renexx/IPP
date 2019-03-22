#!/usr/bin/env python3
#
# Project: Project for Principles of Programming Languages subject
# @file interpret.php
# autor René Bolf
import sys
import xml.etree.ElementTree as ElementTree
import re

def errorMessage(message,exitCode):
    print("ERR: " + message + "\n", file = sys.stderr)
    sys.exit(exitCode)
    
def showHelp():
     print("doplnit")
     sys.exit(0)

if len(sys.argv) > 3 and len(sys.argv) < 2 :
    errorMessage("Wrong count of arguments",10)
    
elif len(sys.argv) == 2 :
    if(sys.argv[1] == "--help"):
        showHelp()
  
    elif(sys.argv[1].startswith("--source=")):
        argv_source = sys.argv[1].split("--source=")[1]
        
    elif(sys.argv[1].startswith("--input=")):
        argv_input = sys.argv[1].split("--input=")[1]
        
    else:
        errorMessage("Bad arguments",10)
            
elif len(sys.argv) == 3:
    if(sys.argv[1].startswith("--source=") and sys.argv[2].startswith("--input=")):
        argv_source = sys.argv[1].split("--source=")[1]
        argv_input = sys.argv[2].split("--input=")[1]
        
    elif(sys.argv[1].startswith("--input=") and sys.argv[2].startswith("source=")):    
        argv_input = sys.argv[1].split("--input=")[1]
        argv_source = sys.argv[2].split("--source=")[1]
        
    else:
        errorMessage("Bad arguments",10)
else:
    errorMessage("Bad arguments",10)        

try:
    dom = ElementTree.parse(argv_source) #object
except OSError as error:
    errorMessage(error.args[1],11) #vyhodenie except ked otvaras subor
except ElementTree.ParseError as error:
    errorMessage(error.args[0],31) #ked nieje well formated

root = dom.getroot()#root program

if(root.tag != "program"):
    errorMessage("In XML is wrong root tag use --help",32)

if len(root.attrib) > 3:
    errorMessage("Many arguments",32)
    
if "language" in root.attrib:   
    if root.attrib["language"] != "IPPcode19":
        errorMessage("Missing header IPPcode19",32)
else:
    errorMessage("Missing element language",32)        
if len(root.attrib) == 2:
    if "description" not in root.attrib  and "name" not in root.attrib:
        errorMessage("Wrong attributes in xml",32)   
if len(root.attrib) == 3:
    if "description" not in root.attrib  or "name" not in root.attrib:        
        errorMessage("Wrong attributes in xml",32)   
    
    
    
    #dom.findall(to co chcem najst vsetky mohol by som takto vyhladat a nejakou funkciu zoradit)


