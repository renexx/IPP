#!/usr/bin/env python3
#
# Project: Project for Principles of Programming Languages subject
# @file interpret.php
# autor René Bolf xbolfr00@stud.fit.vutbr.cz
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

root_program = dom.getroot()#root program

if(root_program.tag != "program"):
    errorMessage("In XML is wrong root tag use --help",32)

if len(root_program.attrib) > 3:
    errorMessage("Many arguments",32)
    
if "language" in root_program.attrib:   
    if root_program.attrib["language"] != "IPPcode19":
        errorMessage("Missing header IPPcode19",32)
else:
    errorMessage("Missing element language",32)        
if len(root_program.attrib) == 2:
    if "description" not in root_program.attrib  and "name" not in root_program.attrib:
        errorMessage("Wrong attributes in xml",32)   
if len(root_program.attrib) == 3:
    if "description" not in root_program.attrib  or "name" not in root_program.attrib:        
        errorMessage("Wrong attributes in xml",32)   

reg_variable = "^(LF|GF|TF)@([a-zA-Z]|[_|\-|\$|&|%|\?|\!|\*])([a-zA-Z]|[0-9]|[_|\-|\$|&|%|\?|\!|\*])*$"
reg_label = "^([a-zA-Z]|[_|\-|\$|&|%|\?|\!|\*])([a-zA-Z]|[0-9]|[_|\-|\$|&|%|\?|\!|\*])*$"
reg_type = "^(int|string|bool)$"    

def symbolCheck(attribType,operand):
    if(attribType == "int"):
        check_symbolint = re.search("^((\+|-)?[0-9]\d*)$",operand)
        if not check_symbolint:
            errorMessage("Zle zapisany typ: int",32)
    elif(attribType == "string"):
        check_symbolstring = re.search("([^\ \\\\#]|\\\\[0-9]{3})*$",operand)
        if not check_symbolstring:
            errorMessage("Zle zapisany typ: string",32)
    elif(attribType == "bool"):
        check_symbolbool = re.search("^(true|false)$",operand)
        if not check_symbolbool:
            errorMessage("Zle zapisany typ: bool",32)
    elif(attribType == "nil"):
        check_symbolnil =  re.search("^nil$",operand) 
        if not check_symbolnil:
            errorMessage("Zle zapisany typ: nil",32)
    elif(attribType == "var"):
        check_var = re.search("^(LF|GF|TF)@([a-zA-Z]|[_|\-|\$|&|%|\?|\!|\*])([a-zA-Z]|[0-9]|[_|\-|\$|&|%|\?|\!|\*])*$",operand)
        if not check_var:
            errorMessage("Zle zapisany typ: var",32)
    else:
        errorMessage("chybny symbol",32) 
        
def variableCheck(attribType,operand):
    if(attribType == "var"):
        check_var = re.search("^(LF|GF|TF)@([a-zA-Z]|[_|\-|\$|&|%|\?|\!|\*])([a-zA-Z]|[0-9]|[_|\-|\$|&|%|\?|\!|\*])*$",operand)
        if not check_var:
            errorMessage("Zle zapisany typ: var",32)
            
def labelCheck(attribType,operand):
    if(attribType == "label"):
        check_label = re.search("^([a-zA-Z]|[_|\-|\$|&|%|\?|\!|\*])([a-zA-Z]|[0-9]|[_|\-|\$|&|%|\?|\!|\*])*$",operand)
        if not check_label:
            errorMessage("Zle zapisany typ: label",32)
            
def typeCheck(attribType,operand):
    if(attribType == "type"):
        check_type = re.search("^(int|string|bool)$",operand)
        if not check_type:
            errorMessage("Zle napisany typ: type",32)
    
    
#TODO analyza xml
#KONTROLA ELEMENTU instruction či tam je a či obsahuje opcode a order
for instruction in root_program:
    if(instruction.tag != "instruction"):
        errorMessage("Missing instruction element",32)
  
    if(len(instruction.attrib) != 2):
        errorMessage("zly pocet atributov",32)
    else:
        if "order" not in instruction.attrib or "opcode" not in instruction.attrib:
            errorMessage("chyba order alebo opcode",32)
###################################################################################
#KONTROLA JEDNOTLIVYCH opcode
# ZACNEME tymi čo maju 0 operandov
# 0 operandov CREATEFRAME PUSHFRAME POPFRAME RETURN break
    if instruction.attrib["opcode"] in ["CREATEFRAME","PUSHFRAME","POPFRAME","RETURN","BREAK"]: #something like switch
        for argument in instruction:
            if(argument.tag != 0):
                errorMessage("zly pocet argumentov u CREATEFRAME,PUSHFRAME,POPFRAME,RETURN,BREAK",32)
###################################################################################################################                
# 1 operand  [var]  DEFVAR, POPS TODO ked mas v instukci arg1 arg1
    elif instruction.attrib["opcode"] in ["DEFVAR","POPS"]:
        counter_arg = 0
        for argument in instruction:
            if "type" not in argument.attrib:
                errorMessage("Chyba type u DEFVAR,POPS",32)
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "var"):
                    errorMessage("Pri DEFVAR a POPS musi byt var",32)
                else:    
                    variableCheck(argument.attrib["type"],argument.text)
            else:
                errorMessage("Zly argument u DEFVAR,POPS",32)
            counter_arg += 1
        if(counter_arg != 1):
            errorMessage("Zly pocet argumentov u DEFVAR,POPS",32)            
                #print(argument.attrib)    #toto je type var
            #print(argument.tag)  # arg1
# 1 operand [symb] = int, string, bool, nil PUSHS, WRITE,EXIT,DPRINT
    elif instruction.attrib["opcode"] in ["PUSHS","WRITE","EXIT","DPRINT"]:
        counter_arg = 0
        for argument in instruction:
            if "type" not in argument.attrib:
                errorMessage("Chyba type u PUSHS, WRITE ,EXIT,DPRINT",32)
            if(argument.tag == "arg1"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri PUSHS, WRITE, EXIT a DPRINT musi byt bud int, string, bool,nil alebo to moze byt var ",32)                                       
                else:    
                    symbolCheck(argument.attrib["type"],argument.text)
            else:
                errorMessage("Zly argument u PUSHS, WRITE ,EXIT,DPRINT",32)
            counter_arg += 1
        if(counter_arg != 1):
            errorMessage("Zly pcoet argumentov u PUSH,WRITE,EXIT,DPRINT",32)             
# 1 operand [label] CALL, LABEL, JUMP
    elif instruction.attrib["opcode"] in ["CALL","LABEL","JUMP"]:
        counter_arg = 0
        for argument in instruction:
            if "type" not in argument.attrib:
                errorMessage("Chyba type u CALL,LABEL,JUMP",32)
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "label"):
                    errorMessage("Pri CALL, LABEL a JUMP musi byt label",32)
                else:
                    labelCheck(argument.attrib["type"],argument.text)    
            else:
                errorMessage("Zly argument u CALL LABEl A JUMP",32)
            counter_arg +=1
        if(counter_arg != 1):
            errorMessage("Zly pocet argumentov u CALL LABEL A JUMP",32)          
# 2 operandy [var][symb]-int,string,bool,nil MOVE,INT2CHAR,TYPE,STRLEN
    elif instruction.attrib["opcode"] in ["MOVE","INT2CHAR","TYPE","STRLEN"]:
        counter_arg = 0
        for argument in instruction:
            if "type" not in argument.attrib:
                errorMessage("Chyba type u MOVE,INT2CHAR,TYPE,STRLEN",32)
            counter_arg += 1
        if(counter_arg != 2):
            errorMessage("Zly pocet argumentov u MOVE,INT2CHAR,TYPE,STRLEN",32)                        
# 2 operandy [var][type] READ
    elif instruction.attrib["opcode"] in ["READ"]:
        counter_arg = 0
        for argument in instruction:
            if "type" not in argument.attrib:
                errorMessage("Chyba type u READ",32)
            counter_arg +=1
        if(counter_arg != 2):
            errorMessage("Zly pocet argumentov u READ",32)
#3 operandy [var] [symb1] [symb2] symbol moze byt var, int, string, bool, nil ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR
    elif instruction.attrib["opcode"] in ["ADD","SUB","MUL","IDIV","LT","GT","EQ","AND","OR","NOT","STRI2INT","CONCAT","GETCHAR","SETCHAR"]:
        counter_arg = 0
        for argument in instruction:
            if "type" not in argument.attrib:
                errorMessage("Chyba type u ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR ",32)
            counter_arg += 1
        if(counter_arg != 3):
            errorMessage("Zly pocet argumentov u ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR",32) 
                  
#3 oprandy [label] [symb1] [symb2]   JUMPIFEQ JUMPIFNEQ           
    elif instruction.attrib["opcode"] in ["JUMPIFEQ","JUMPIFNEQ"]:
        counter_arg = 0
        for argument in instruction:
            if "type" not in argument.attrib:
                errorMessage("Chyba type u JUMPIFEQ, JUMPIFNEQ ",32)
            counter_arg += 1
        if(counter_arg != 3):
            errorMessage("Zly pocet argumentov u JUMPIFEQ a JUMPIFNEQ",32) 
    else:
        errorMessage("Neznamy operacny kod",32)

#zoradenie xmlka
root_program[:] = sorted(root_program, key=lambda child: int(child.get("order")))
for child in root_program:
    child[:] = sorted(child, key =lambda child: child.tag)
    
counter_order = 1
for instruction in root_program:
    if int(instruction.get("order")) != counter_order:
        errorMessage("Zly order, order musi zacitat od 1",32)
# TOTO PRETO ABY NEBOLO PRI DAKEJ INSTRUKCI arg1 arg1##########################        
    if instruction.attrib["opcode"] in ["MOVE","INT2CHAR","TYPE","STRLEN","READ"]:    
        if(instruction[0].tag != "arg1" or instruction[1].tag != "arg2"):
            errorMessage("Zle poradie argumentov u MOVE, INT2CHAR, TYPE, STRLEN, READ",32)
    if instruction.attrib["opcode"] in ["ADD,SUB","MUL","IDIV","LT","GT","EQ","AND","OR","NOT","STRI2INT","CONCAT","GETCHAR","SETCHAR"]:
        if(instruction[0].tag != "arg1" or instruction[1].tag != "arg2" or instruction[2].tag != "arg3"):
            errorMessage("Zle poradie argumentov u ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR",32)
# 2 operandy [var][symb]-int,string,bool,nil MOVE,INT2CHAR,TYPE,STRLEN            
    if instruction.attrib["opcode"] in ["MOVE","INT2CHAR","TYPE","STRLEN"]:                 
        for argument in instruction:
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "var"):
                    errorMessage("Pri MOVE,INT2CHAR,TYPE,STRLEN musi byt arg1 var",32)
                else:
                    variableCheck(argument.attrib["type"],argument.text)
            elif(argument.tag == "arg2"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri MOVE,INT2CHAR,TYPE,STRLEN musi byt arg2 int,string,bool,nil alebo to moze byt var",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)    
            else:
                errorMessage("Zle argumenty u MOVE,INT2CHAR,TYPE,STRLEN",32)
# 2 operandy [var][type] READ                
    elif instruction.attrib["opcode"] in ["READ"]: 
        for argument in instruction:
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "var"):
                    errorMessage("Pri READ musi byt arg1 var",32)
                else:
                    variableCheck(argument.attrib["type"],argument.text)    
            elif(argument.tag == "arg2"):
                if(argument.attrib["type"] != "type"):
                    errorMessage("Pri READ musi byt arg2 type",32)
                else:
                    typeCheck(argument.attrib["type"],argument.text)    
            else:
                errorMessage("Zle argumenty u READ",32)
#3 operandy [var] [symb1] [symb2] symbol moze byt var, int, string, bool, nil ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR
    elif instruction.attrib["opcode"] in ["ADD","SUB","MUL","IDIV","LT","GT","EQ","AND","OR","NOT","STRI2INT","CONCAT","GETCHAR","SETCHAR"]:            
        for argument in instruction:
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "var"):
                    errorMessage("Pri ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR musi byt arg1 var",32)
                else:
                    variableCheck(argument.attrib["type"],argument.text)    
            elif(argument.tag == "arg2"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR musi byt arg2 int,string,bool,nil,var",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)    
            elif(argument.tag == "arg3"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR musi byt arg3 int,string,bool,nil,var",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)                                                    
            else:
                errorMessage("Zle argumenty u ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR",32)
#3 oprandy [label] [symb1] [symb2]   JUMPIFEQ JUMPIFNEQ 
    elif instruction.attrib["opcode"] in ["JUMPIFEQ","JUMPIFNEQ"]:
        for argument in instruction:
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "label"):
                    errorMessage("Pri JUMPIFEQ a JUMPIFNEQ musi byt arg1 label",32)
                else:
                    labelCheck(argument.attrib["type"],argument.text)    
            elif(argument.tag == "arg2"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri JUMPIFEQ a JUMPIFNEQ musi byt arg2 int,string,bool,nil,var",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)    
            elif(argument.tag == "arg3"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri JUMPIFEQ a JUMPIFNEQ musi byt arg3 int,string,bool,nil,var",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)                                                    
            else:
                errorMessage("Zle argumenty u JUMPIFEQ a JUMPIFNEQ",32)
   

    counter_order += 1
    
class frames:    
    GF = {} # vytvorenie slovnika pre GF ramec teda globalny ramec
    TF = None # temporary frame si nastavíme zatial na none čiže neni defined
    LF = []
    dataStack = []
    callStack = []

    def identifFrame(variable,value,typ):
        frame = variable.split("@",1)[0]
        variableName = variable.split("@",1)[1]
        if frame == "GF":
            GF[variableName] = [value,typ]
        if frame == "TF":
            if TF == None:
                errorMessage("Pristup k nedefinovanemu ramcu",55)
            else:
                TF[variableName] = [value,typ]
        if frame == "LF":
            if LF:
                LF[-1][variableName] = [value,typ]
            else:
                errorMessage("Pristup k nedefinovanemu ramcu",55)  
                   
    def getVar(variable):
        frame = variable.split("@",1)[0]
        variableName = variable.split("@",1)[1]
        if frame == "GF":
            return GF.get(variableName)
        if frame == "TF":
            if TF == None:
                errorMessage("Pristup k nedefinovanemu ramcu",55)
            else:
                return TF.get(VariableName)
        if frame == "LF":
            if LF:
                return LF[-1].get(VariableName)
            else:
                errorMessage("Pristup k nedefinovanemu ramcu",55)   
            
    
    for instruction in root_program:
        print(instruction[0].text)
        variableName = instruction[0].text
        variableNamesplited = variableName.split("@",1)
        print(variableName)
        frame = variableNamesplited[0]
        variable = variableNamesplited[1]           
        if instruction.attrib["opcode"] == "ADD":
            #print(instruction[0].text)
            print("ADD")
            print(instruction[1].text)
            print(instruction[2].text)
            if instruction[1].attrib["type"] == "var":
                var = getVar(instruction[1].text)
                if var[0] == "int" and instruction[2].attrib["type"] == "int":
                    result = int(var[1]) + int(instruction[2].text)
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)      
            elif instruction[2].attrib["type"] == "var":
                var = getVar(instruction[2].text)
                if var[0] == "int" and instruction[1].attrib["type"] == "int":
                    result = int(var[1]) + int(instruction[1].text)
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)   
                    
            elif instruction[1].["type"].attrib == "var" and instruction[2].attrib["type"] == "var":
                var1 = getVar(instruction[1].text) # 0. - typ      1. - hodnota
                var2 = getVar(instruction[2].text) # 0. - typ      1. - hodnota
                if var1[0] == "int" and var2[0] == "int"
                    result = int(var1[1]) + int(var2[1])
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("",32)    
            else:
                if instruction[1].attrib["type"] == "int" and instruction[2].attrib["type"] == "int":        
                    result = int(instruction[1].text) + int(instruction[2].text)
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)
                        
        elif instruction.attrib["opcode"] == "SUB":
            print("SUB")
            print(instruction[1].text)
            print(instruction[2].text)
            if instruction[1].attrib["type"] == "var":
                var = getVar(instruction[1].text)
                if var[0] == "int" and instruction[2].attrib["type"] == "int":
                    result = int(var[1]) - int(instruction[2].text)
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)      
            elif instruction[2].attrib["type"] == "var":
                var = getVar(instruction[2].text)
                if var[0] == "int" and instruction[1].attrib["type"] == "int":
                    result = int(var[1]) - int(instruction[1].text)
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)   
                    
            elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
                var1 = getVar(instruction[1].text) # 0. - typ      1. - hodnota
                var2 = getVar(instruction[2].text) # 0. - typ      1. - hodnota
                if var1[0] == "int" and var2[0] == "int"
                    result = int(var1[1]) - int(var2[1])
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("",32)    
            else:
                if instruction[1].attrib["type"] == "int" and instruction[2].attrib["type"] == "int":        
                    result = int(instruction[1].text) - int(instruction[2].text)
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)
        elif instruction.attrib["opcode"] == "MUL":
            print("MUL")
            print(instruction[1].text)
            print(instruction[2].text)
            if instruction[1].attrib["type"] == "var":
                var = getVar(instruction[1].text)
                if var[0] == "int" and instruction[2].attrib["type"] == "int":
                    result = int(var[1]) * int(instruction[2].text)
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)      
            elif instruction[2].attrib["type"] == "var":
                var = getVar(instruction[2].text)
                if var[0] == "int" and instruction[1].attrib["type"] == "int":
                    result = int(var[1]) * int(instruction[1].text)
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)   
                    
            elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
                var1 = getVar(instruction[1].text) # 0. - typ      1. - hodnota
                var2 = getVar(instruction[2].text) # 0. - typ      1. - hodnota
                if var1[0] == "int" and var2[0] == "int"
                    result = int(var1[1]) * int(var2[1])
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("",32)    
            else:
                if instruction[1].attrib["type"] == "int" and instruction[2].attrib["type"] == "int":        
                    result = int(instruction[1].text) * int(instruction[2].text)
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)
        elif instruction.attrib["opcode"] == "IDIV":
            print("IDIV")
            if instruction[1].attrib["type"] == "var":
                var = getVar(instruction[1].text)
                if var[0] == "int" and instruction[2].attrib["type"] == "int":
                    if int(var[1]) == 0 or int(instruction[2].text) == 0:
                        errorMessage("delenie nulou",57)
                    else:    
                        result = int(var[1]) // int(instruction[2].text)
                        identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)      
            elif instruction[2].attrib["type"] == "var":
                var = getVar(instruction[2].text)
                if var[0] == "int" and instruction[1].attrib["type"] == "int":
                    if int(var[1]) == 0 or int(instruction[2].text) == 0:
                        errorMessage("delenie nulou",57)
                    else:    
                        result = int(var[1]) // int(instruction[1].text)
                        identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)   
                    
            elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
                var1 = getVar(instruction[1].text) # 0. - typ      1. - hodnota
                var2 = getVar(instruction[2].text) # 0. - typ      1. - hodnota
                if var1[0] == "int" and var2[0] == "int":
                    if int(var1[1]) == 0 or int(var2[1]) == 0:
                        errorMessage("delenie nulou",57)
                    else:    
                        result = int(var1[1]) // int(var2[1])
                        identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("",32)    
            else:
                if instruction[1].attrib["type"] == "int" and instruction[2].attrib["type"] == "int":  
                    if int(instruction[1].text) == 0 or int(instruction[2].text) == 0:
                        errorMessage("delenie nulou",57)
                    else:        
                        result = int(instruction[1].text) // int(instruction[2].text)
                        identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)
        elif instruction.attrib["opcode"] in ["LT","GT","EQ"]:
                if instruction[1].attrib["type"] != instruction[2].attrib["type"]:        
                    errorMessage("nekopatibilne typy",32)
                else:
                    if instruction.attrib["opcode"] in ["LT","GT"]:    
                        if instruction[1].attrib["type"] == "nil" or instruction[2].attrib["type"] == "nil":
                            errorMessage("nemozno porovnavat pri LT a EQ nil",53)
                        else:    
                            if instruction.attrib["opcode"] == "LT":    
                                print("LT")
                                if instruction[1].attrib["type"] == "var":
                                    var = getVar(instruction[1].text)
                                    result = var[1] < instruction[2].text
                                    identifFrame(instruction[0].text,"bool",result)
                                elif instruction[2].attrib["type"] == "var":
                                    var = getVar(instruction[2].text)
                                    result = var[1] < instruction[1].text
                                    identifFrame(instruction[0].text,"bool",result)
                                elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
                                    var1 = getVar(instruction[1].text) # 0. - typ      1. - hodnota
                                    var2 = getVar(instruction[2].text) # 0. - typ      1. - hodnota
                                    result = var1[1] < var2[1]
                                    identifFrame(instruction[0].text,"bool",result)        
                                else:    
                                    result = instruction[1].text < instruction[2].text     
                                    identifFrame(instruction[0].text,"bool",result)   
                                    print("\n")
                            elif instruction.attrib["opcode"] == "GT":
                                print("GT")
                                if instruction[1].attrib["type"] == "var":
                                    var = getVar(instruction[1].text)
                                    result = var[1] > instruction[2].text
                                    identifFrame(instruction[0].text,"bool",result
                                elif instruction[2].attrib["type"] == "var":
                                    var = getVar(instruction[2].text)
                                    result = var[1] > instruction[1].text
                                    identifFrame(instruction[0].text,"bool",result)
                                elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
                                    var1 = getVar(instruction[1].text) # 0. - typ      1. - hodnota
                                    var2 = getVar(instruction[2].text) # 0. - typ      1. - hodnota
                                    result = var1[1] > var2[1]
                                    identifFrame(instruction[0].text,"bool",result)        
                                else:
                                    result = instruction[1].text > instruction[2].text     
                                    identifFrame(instruction[0].text,"bool",result) 
                                    print("\n")
                    elif instruction.attrib["opcode"] == "EQ":
                        print("EQ")
                        if instruction[1].attrib["type"] == "var":
                            var = getVar(instruction[1].text)
                            result = var[1] == instruction[2].text
                            identifFrame(instruction[0].text,"bool",result
                        elif instruction[2].attrib["type"] == "var":
                            var = getVar(instruction[2].text)
                            result = var[1] == instruction[1].text
                            identifFrame(instruction[0].text,"bool",result
                        elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
                            var1 = getVar(instruction[1].text) # 0. - typ      1. - hodnota
                            var2 = getVar(instruction[2].text) # 0. - typ      1. - hodnota
                            result = var1[1] == var2[1]
                            identifFrame(instruction[0].text,"bool",result)        
                        else:
                            result = instruction[1].text == instruction[2].text     
                            identifFrame(instruction[0].text,"bool",result)
                if instruction.attrib["opcode"] == "EQ":
                    if instruction[1].attrib["type"] == "nil" or instruction[2].attrib["type"] == "nil": 
                        if instruction[1].attrib["type"] == "var":
                            var = getVar(instruction[1].text)
                            result = var[1] == instruction[2].text
                            identifFrame(instruction[0].text,"bool",result
                        elif instruction[2].attrib["type"] == "var":
                            var = getVar(instruction[2].text)
                            result = var[1] == instruction[1].text
                            identifFrame(instruction[0].text,"bool",result) 
                        elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
                            var1 = getVar(instruction[1].text) # 0. - typ      1. - hodnota
                            var2 = getVar(instruction[2].text) # 0. - typ      1. - hodnota
                            result = var1[1] == var2[1]
                            identifFrame(instruction[0].text,"bool",result)       
                        else:    
                            result = instruction[1].text == instruction[2].text     
                            identifFrame(instruction[0].text,"bool",result)
                            print("\n")    
        elif instruction.attrib["opcode"] == "AND":
                if instruction[1].attrib["type"] == "var":
                    var = getVar(instruction[1].text)
                    if var[0] == "bool" and instruction[2].attrib["type"] == "bool":    
                        result = bool(var[1]) and bool(instruction[2].text)
                        identifFrame(instruction[0].text,"bool",result)
                    else:
                        errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)      
                elif instruction[2].attrib["type"] == "var":
                    var = getVar(instruction[2].text)
                    if var[0] == "bool" and instruction[1].attrib["type"] == "bool":    
                        result = bool(var[1]) and bool(instruction[1].text)
                        identifFrame(instruction[0].text,"bool",result)
                    else:
                        errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)   
                        
                elif instruction[1].attrib["type"] == "bool" and instruction[2].attrib["type"] == "bool":
                    var1 = getVar(instruction[1].text) # 0. - typ      1. - hodnota
                    var2 = getVar(instruction[2].text) # 0. - typ      1. - hodnota
                    if var1[0] == "bool" and var2[0] == "bool":    
                        result = bool(var1[1]) and bool(var2[1])
                        identifFrame(instruction[0].text,"bool",result)
                    else:
                        errorMessage("",32)    
                else:
                    if instruction[1].attrib["type"] == "bool" and instruction[2].attrib["type"] == "bool":          
                        result = bool(instruction[1].text) and bool(instruction[2].text)
                        identifFrame(instruction[0].text,"bool",result)
                    else:
                        errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)
        elif instruction.attrib["opcode"] == "OR":
                if instruction[1].attrib["type"] == "var":
                    var = getVar(instruction[1].text)
                    if var[0] == "bool" and instruction[2].attrib["type"] == "bool":    
                        result = bool(var[1]) or bool(instruction[2].text)
                        identifFrame(instruction[0].text,"bool",result)
                    else:
                        errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)      
                elif instruction[2].attrib["type"] == "var":
                    var = getVar(instruction[2].text)
                    if var[0] == "bool" and instruction[1].attrib["type"] == "bool":    
                        result = bool(var[1]) or bool(instruction[1].text)
                        identifFrame(instruction[0].text,"bool",result)
                    else:
                        errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)   
                        
                elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
                    var1 = getVar(instruction[1].text) # 0. - typ      1. - hodnota
                    var2 = getVar(instruction[2].text) # 0. - typ      1. - hodnota
                    if var1[0] == "bool" and var2[0] == "bool":    
                        result = bool(var1[1]) or bool(var2[1])
                        identifFrame(instruction[0].text,"bool",result)
                    else:
                        errorMessage("",32)    
                else:
                    if instruction[1].attrib["type"] == "bool" and instruction[2].attrib["type"] == "bool":          
                        result = bool(instruction[1].text) or bool(instruction[2].text)
                        identifFrame(instruction[0].text,"bool",result)
                    else:
                        errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)
        elif instruction.attrib["opcode"] == "NOT":
                if instruction[1].attrib["type"] == "var":
                    var = getVar(instruction[1].text)
                    if var[0] == "bool":    
                        result = not bool(var[1])
                        identifFrame(instruction[0].text,"bool",result)
                    else:
                        errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)                          
                else:
                    if instruction[1].attrib["type"] == "bool":          
                        result = not bool(instruction[1].text)
                        identifFrame(instruction[0].text,"bool",result)
                    else:
                        errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)
                      
        elif instruction.attrib["opcode"] == "INT2CHAR":
            if instruction[1].attrib["type"] == "var":
                var = getVar(instruction[1].text)
                if var[0] == "int":    
                    value = int(instruction[1].text)
                    try:
                        result = chr(value)
                        identifFrame(instruction[0].text,"int",result)
                    except ValueError as error:
                        errorMessage(error.args[0],58)
                else:
                    errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)
            else:
                if instruction[1].attrib["type"] == "int":
                    value = int(instruction[1].text)
                    try:
                        result = chr(value)
                        identifFrame(instruction[0].text,"int",result)
                    except ValueError as error:
                        errorMessage(error.args[0],58)
                else:
                    errorMessage("zle zle zle",32)   
            
        elif instruction.attrib["opcode"] == "STRI2INT":
            print("STRI2INT")
            if instruction[1].attrib["type"] == "var":
                var = getVar(instruction[1].text)
                if var[0] == "string" and instruction[2].attrib["type"] == "int":
                    var[1] = instruction[1].text
                    intValue = int(instruction[2].text)
                    if 0 <= intValue < len(var[1]):
                        ordasci = [ord(c) for c in var[1]]
                        result = ordasci[intValue]
                        identifFrame(instruction[0].text,"int",result)
                    else:
                        errorMessage("Mimo rozsah u SETCHAR",58) 
                else:
                    errorMessage("Zle zadane typy pri STRI2INT",32) 
            elif instruction[2].attrib["type"] == "var":
                var = getVar(instruction[2].text)
                if var[0] == "string" and instruction[1].attrib["type"] == "int":
                    var[1] = instruction[2].text
                    intValue = int(instruction[1].text)
                    if 0 <= intValue < len(var[1]):
                        ordasci = [ord(c) for c in var[1]]
                        result = ordasci[intValue]
                        identifFrame(instruction[0].text,"int",result)
                    else:
                        errorMessage("Mimo rozsah u SETCHAR",58) 
                else:
                    errorMessage("Zle zadane typy pri STRI2INT",32)         
            elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
                var1 = getVar(instruction[1].text)
                var2 = getVar(instruction[2].text)
                if var1[0] == "string" and var2[0] == "int":
                    var1[1] = instruction[1].text
                    var2[1] = int(instruction[2].text)
                    if 0 <= var2[1] < len(var[1]):
                        ordasci = [ord(c) for c in var1[1]]
                        result = ordasci[var2[1]]
                        identifFrame(instruction[0].text,"int",result)
                    else:
                        errorMessage("Mimo rozsah u SETCHAR",58) 
                else:
                    errorMessage("Zle zadane typy pri STRI2INT",32)         
            else:    
                if instruction[1].attrib["type"] == "string" and instruction[2].attrib["type"] == "int":
                    stringValue = instruction[1].text
                    intValue = int(instruction[2].text)
                    if 0 <= intValue < len(stringValue):
                        ordasci = [ord(c) for c in stringValue]
                        result = ordasci[intValue]
                        identifFrame(instruction[0].text,"int",result)
                    else:
                        errorMessage("Mimo rozsah u SETCHAR",58) 
                else:
                    errorMessage("Zle zadane typy pri STRI2INT",32)           
                
        elif instruction.attrib["opcode"] == "EXIT":
                if instruction[0].attrib["type"] == "int":
                    exitInt = int(instruction[0].text) 
                elif instruction[0].attrib["type"] == "var":
                    var = getVar(instruction[0].text)
                    if var[0] == "int":
                        exitInt = int(var[1])
                    else:
                        errorMessage("",32)                        
                else:
                     errorMessage("EXIT musi byt int alebo var",32)
                if 0 <= exitInt <= 49:
                    sys.exit(exitInt)
                else:
                    errorMessage("Spatna ciselna hodnota instrukcie EXIT",57)       

        elif instruction.attrib["opcode"] == "CONCAT": # <var> <symb1> <symb2>
            if instruction[1].attrib["type"] == "var":
                var = getVar(instruction[1].text)
                if var[0] == "string" and instruction[2].attrib["type"] == "string":
                    result = var[1] + instruction[2].text
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("ERROR",32)
            elif instruction[2].attrib["type"] == "var":
                var = getVar(instruction[2].text)    
                if var[0] == "string" and instruction[1].attrib["type"] == "string":    
                    result = var[1] + instruction[1].text
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("ERROR",32)    
            elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var": 
                var1 = getVar(instruction[1].text) 
                var2 = getVar(instruction[2].text) 
                if var1[0] == "string" and var2[0] == "string":
                    result = var1[1] + var2[1]
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("ERROR",32)       
            else:
                  if instruction[1].attrib["type"] != "string" or instruction[2].attrib["type"] != "string":
                      errorMessage("pri CONCAT musi byt symb1 aj symb2 type: string",32)     
                  else:
                     result = instruction[1].text + instruction[2].text
                     identifFrame(instruction[0].text,"int",result)
                 
        elif instruction.attrib["opcode"] == "STRLEN":
            if instruction[1].attrib["type"] != "string":
                errorMessage("Zly typ pri STRLEN, symb1 musi byt string",32)
            else:
                print("STRLEN")
                print(instruction[1].text)            
                instruction[0].text = int(len(instruction[1].text))   
                print(instruction[0].text) 
                print("\n")  
        elif instruction.attrib["opcode"] == "GETCHAR":
                print("GETCHAR")
                print(instruction[1].text)
                print(instruction[2].text)    
                if instruction[1].attrib["type"] == "string" and instruction[2].attrib["type"] == "int":
                    stringValue = instruction[1].text
                    intValue = int(instruction[2].text)
                    varValue = instruction[0].text
                    if 0 <= intValue < len(stringValue):
                        listStringvalue = list(stringValue)
                        varValue = listStringvalue[intValue]
                        print(varValue)
                    else:
                        errorMessage("Mimo rozsah u GETCHAR",58)
                else:
                     errorMessage("zle zadane typy pri GETCHAR, symb1 ma byt string, symb2 : int",32)
        elif instruction.attrib["opcode"] == "TYPE": # <var> <symb>
            print("TYPE")
            print(instruction[1].text)
            boola = instruction[1].text
            print(type(boola))
            #typ = instruction[1].text
            
            #if type(int(typ)) is int:
            #    instruction[0].text = "int"
            #    print(instruction[0].text)                
            #elif type(bool) is bool:
            #    instruction[0].text = "bool"
            #    print(instruction[0].text) 
            #elif type(typ) is str:
            #     typ = "string"
            #     instruction[0].text = typ
            #     print(instruction[0].text)   
            #else:
            #    errorMessage("zly typ",32)     

                
        elif instruction.attrib["opcode"] == "DPRINT":
            print("DPRINT")
            if instruction[0].attrib["type"] == "string":
                sys.stderr.write(instruction[0].text)
            elif instruction[0].attrib["type"] == "bool":
                if instruction[0].text == "false":
                   sys.stderr.write(instruction[0].text)
                else:
                    sys.stderr.write(instruction[0].text)
            elif instruction[0].attrib["type"] == "int":
                sys.stderr.write(instruction[0].text)
            elif instruction[0].attrib["type"] == "var":
                var = instruction[0].text
                var_sp = var.split("@",1)
                sys.stderr.write(var_sp[1])
        elif instruction.attrib["opcode"] == "BREAK":
            pass
        #elif instruction.attrib["opcode"] == "MOVE": #<var> <symb>TODO
        elif instruction.attrib["opcode"] == "CREATEFRAME":
            print("CREATEFRAME")
            TF = {}
            print("TOTO JE DOCASTNY RAMEC")
            print(TF)
        elif instruction.attrib["opcode"] == "PUSHFRAME":
            LF.append(TF)
            TF = None
            if TF == None:
                errorMessage("Pristup k nedefinovanemu ramcu",55)
                              
        elif instruction.attrib["opcode"] == "POPFRAME":
            try:
                TF = LF.pop()
            except IndexError as err:
                errorMessage(err.args[0],55) 
                   
        elif instruction.attrib["opcode"] == "DEFVAR":
            if frame == "GF":
                GF[variable] = None
            if frame == "TF":
                if TF == None:
                    errorMessage("Pristup k nedefinovanemu ramcu",55)
                else:
                    TF[variable] = None
            if frame == "LF":
                if LF:
                    LF[-1][variable] = None
                else:
                    errorMessage("Pristup k nedefinovanemu ramcu",55)                
                    
        #elif instruction.attrib["opcode"] == "CALL": TODO
        #elif instruction.attrib["opcode"] == "RETURN": TODO                
        elif instruction.attrib["opcode"] == "PUSHS":
            dataStack.append(instruction[0].text)
        elif instruction.attrib["opcode"] == "POPS":
            try:
                dataStack.pop(inst)
            except IndexError as err:
                errorMessage(err.args[0],55)
                   
        #elif instruction.attrib["opcode"] == "READ": #var type 
        #    print("READ") # pre dbuging
        #    print(instruction[0].text) # var
        #    print(instruction[1].text) #type
        #    vstup = input() #nacitanie vstupu
        #    bool = re.search("^true",vstup,re.IGNORECASE) #regulak pre bool hlada true a je jedno ci True alebo true alebo TRUE 
        #    vstup = vstup.split(" ") #nacitany vstup si rozdelime podla medzier
        #    print(vstup) 
        #    if vstup[1] == "string": #ak je ten ahoj string tak je to string  
        #        if vstup[1] == instruction[1].text: #ak je ten vstup rovnaky s xml
        #            instruction[0].text = vstup[0] #do varu ulozime hodnotu ktoru sme nacitali
        #            print(instruction[0].text)
        #            print("si string")
        #        else:
        #            instruction[0].text = ""  #ak neni tak prazdny retazec
        #            print(instruction[0].text)
        #    elif vstup[1] == "int":
        #        if vstup[1] == instruction[1].text:
        #            instruction[0].text = vstup[0]
        #            print(instruction[0].text)
        #            print("si integer")
        #        else:
        #            instruction[0].text = "0"
        #            print(instruction[0].text)
        #    elif vstup[1] == "bool":
        #        if vstup[1] == instruction[1].text:
        #            if bool:
        #                instruction[0].text = vstup[0]
        #                print(instruction[0].text)
        #                print("si true")
        #            else:
        #                instruction[0].text = "false"
        #                print(instruction[0].text)
        #                print("si false")
        #        else:
        #            instruction[0].text = "false"
        #            print(instruction[0].text)        
        #    else:
        #        print("zle zadany typ")                       
        elif instruction.attrib["opcode"] == "WRITE":  #<symb>
            print("WRITE")
            #print(instruction[0].attrib)
            #print("\n")
            #print(instruction[0].text)                               
            if instruction[0].attrib["type"] == "bool":
                if instruction[0].text == "true":
                    print("true",end='')
                else:
                    print("false",end='')
            elif instruction[0].attrib["type"] == "int":
                print(int(instruction[0].text),end='')
            elif instruction[0].attrib["type"] == "string":
                print(instruction[0].text,end='')
            elif instruction[0].attrib["type"] == "string":
                print(instruction[0].text,end='')  
            else:
                errorMessage("Zly typ",32)
        elif instruction.attrib["opcode"] == "LABEL":
            print("LABEL")
            print(instruction[0].text)
            print(instruction.attrib["order"])
            if instruction[0].text in Labels:
                errorMessage("Pokus o redefinaciu uz existujuceho navesti",52)
            else:
                Labels[instruction[0].text] = instruction.attrib["order"]
                print(Labels)
        elif instruction.attrib["opcode"] == "JUMP":
            print("JUMP")
            print(instruction[0].text)
            print(instruction.attrib["order"])        
            if instruction[0].text not in Labels:
                errorMessage("undefined label",52)    
            else:
                pass
        elif instruction.attrib["opcode"] == "CALL":
            print("CALL")
            print(instruction[0].text)
            print(instruction.attrib["order"])
            if instruction[0].text not in Labels:
                errorMessage("undefined label",52)
            else:
                pass                       
               
#dom.write("example.xml")

