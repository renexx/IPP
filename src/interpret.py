#!/usr/bin/env python3
#
# Project: Project for Principles of Programming Languages subject
# @file interpret.php
# autor René Bolf
import sys
import xml.etree.ElementTree as ET
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
        print(argv_source)
    elif(sys.argv[1].startswith("--input=")):
        argv_input = sys.argv[1].split("--input=")[1]
        print(argv_input)
    else:
        errorMessage("Bad arguments",10)
            
elif len(sys.argv) == 3:
    if(sys.argv[1].startswith("--source=") and sys.argv[2].startswith("--input=")):
        argv_source = sys.argv[1].split("--source=")[1]
        argv_input = sys.argv[2].split("--input=")[1]
        print(argv_source)
        print(argv_input)
    elif(sys.argv[1].startswith("--input=") and sys.argv[2].startswith("source=")):    
        argv_input = sys.argv[1].split("--input=")[1]
        argv_source = sys.argv[2].split("--source=")[1]
        print(argv_source)
        print(argv_input)
    else:
        errorMessage("Bad arguments",10)
else:
    errorMessage("Bad arguments",10)        






