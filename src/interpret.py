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
        STDINInput = True
    elif(sys.argv[1].startswith("--input=")):
        argv_input = open(sys.argv[1].split("--input=")[1],"r")
        argv_source = sys.stdin
    else:
        errorMessage("Bad arguments",10)

elif len(sys.argv) == 3:
    if(sys.argv[1].startswith("--source=") and sys.argv[2].startswith("--input=")):
        argv_source = sys.argv[1].split("--source=")[1]
        argv_input = open(sys.argv[2].split("--input=")[1],"r")

    elif(sys.argv[1].startswith("--input=") and sys.argv[2].startswith("source=")):
        argv_input = open(sys.argv[1].split("--input=")[1],"r")
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
    elif instruction.attrib["opcode"] in ["MOVE","INT2CHAR","TYPE","STRLEN","READ","NOT"]:
        counter_arg = 0
        for argument in instruction:
            if "type" not in argument.attrib:
                errorMessage("Chyba type u MOVE,INT2CHAR,TYPE,STRLEN,READ,NOT",32)
            counter_arg += 1
        if(counter_arg != 2):
            errorMessage("Zly pocet argumentov u MOVE,INT2CHAR,TYPE,STRLEN,READ,NOT",32)
#3 operandy [var] [symb1] [symb2] symbol moze byt var, int, string, bool, nil ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR
    elif instruction.attrib["opcode"] in ["ADD","SUB","MUL","IDIV","LT","GT","EQ","AND","OR","STRI2INT","CONCAT","GETCHAR","SETCHAR","JUMPIFEQ","JUMPIFNEQ"]:
        counter_arg = 0
        for argument in instruction:
            if "type" not in argument.attrib:
                errorMessage("Chyba type u ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR,JUMPIFEQ,JUMPIFNEQ",32)
            counter_arg += 1
        if(counter_arg != 3):
            errorMessage("Zly pocet argumentov u ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR,JUMPIFEQ,JUMPIFNEQ",32)


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
    if instruction.attrib["opcode"] in ["MOVE","INT2CHAR","TYPE","STRLEN","READ,NOT"]:
        if(instruction[0].tag != "arg1" or instruction[1].tag != "arg2"):
            errorMessage("Zle poradie argumentov u MOVE, INT2CHAR, TYPE, STRLEN, READ,NOT",32)
    if instruction.attrib["opcode"] in ["ADD,SUB","MUL","IDIV","LT","GT","EQ","AND","OR","STRI2INT","CONCAT","GETCHAR","SETCHAR","JUMPIFEQ","JUMPIFNEQ"]:
        if(instruction[0].tag != "arg1" or instruction[1].tag != "arg2" or instruction[2].tag != "arg3"):
            errorMessage("Zle poradie argumentov u ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR,JUMPIFEQ,JUMPIFNEQ",32)
# 2 operandy [var][symb]-int,string,bool,nil MOVE,INT2CHAR,TYPE,STRLEN
    if instruction.attrib["opcode"] in ["MOVE","INT2CHAR","TYPE","STRLEN,NOT"]:
        for argument in instruction:
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "var"):
                    errorMessage("Pri MOVE,INT2CHAR,TYPE,STRLEN, NOT musi byt arg1 var",32)
                else:
                    variableCheck(argument.attrib["type"],argument.text)
            elif(argument.tag == "arg2"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri MOVE,INT2CHAR,TYPE,STRLEN,NOT musi byt arg2 int,string,bool,nil alebo to moze byt var",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)
            else:
                errorMessage("Zle argumenty u MOVE,INT2CHAR,TYPE,STRLEN,NOT",32)
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
    elif instruction.attrib["opcode"] in ["ADD","SUB","MUL","IDIV","LT","GT","EQ","AND","OR","STRI2INT","CONCAT","GETCHAR","SETCHAR"]:
        for argument in instruction:
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "var"):
                    errorMessage("Pri ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR musi byt arg1 var",32)
                else:
                    variableCheck(argument.attrib["type"],argument.text)
            elif(argument.tag == "arg2"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR musi byt arg2 int,string,bool,nil,var",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)
            elif(argument.tag == "arg3"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR musi byt arg3 int,string,bool,nil,var",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)
            else:
                errorMessage("Zle argumenty u ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR",32)
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


GF = {} # vytvorenie slovnika pre GF ramec teda globalny ramec
TF = None # temporary frame si nastavíme zatial na none čiže neni defined
LF = []
dataStack = []
callStack = []
Labels = {}

def identifFrame(variable,value,typ):
    frame = variable.split("@",1)[0]
    variableName = variable.split("@",1)[1]
    if typ == "string":
        value = replaceEscapeSeq(value)
    if frame == "GF":
        if variableName not in GF:
            errorMessage("variable neni v gf",32)
        else:
            GF[variableName] = [value,typ]
    if frame == "TF":
        if TF == None:
            errorMessage("Pristup k nedefinovanemu ramcu",55)
        elif variableName not in TF:
            errorMessage("variable neni v tf",32)
        else:
            TF[variableName] = [value,typ]
    if frame == "LF":
        if LF:
            LF[-1][variableName] = [value,typ]
        else:
            errorMessage("Pristup k nedefinovanemu ramcu",55)
        if variableName not in LF[-1]:
            errorMessage("variable neni v lf",32)

def getVar(variable):
    frame = variable.split("@",1)[0]
    variableName = variable.split("@",1)[1]
    if frame == "GF":
        if variableName not in GF:
            errorMessage("variable neni v gf",32)
        else:
            return GF.get(variableName)
    if frame == "TF":
        if TF == None:
            errorMessage("Pristup k nedefinovanemu ramcu",55)
        elif variableName not in TF:
            errorMessage("varuable neni v tf",32)
        else:
            return TF.get(variableName)
    if frame == "LF":
        if LF:
            return LF[-1].get(variableName)
        else:
            errorMessage("Pristup k nedefinovanemu ramcu",55)
        if variableName not in LF:
            errorMessage("variable neni v lf",32)

def replaceEscapeSeq(string):
    string1 = re.findall("[0-9]{3}", string)

    for i in string1:
        string = string.replace("\\{0}".format(i) ,chr(int(i)))

    return string

for instruction in root_program:
######################################## LABEL #######################################################
        if instruction.attrib["opcode"] == "LABEL":


            if instruction[0].text in Labels:
                errorMessage("Pokus o redefinaciu uz existujuceho navesti",52)
            else:
                Labels[instruction[0].text] = int(instruction.attrib["order"])

###############################################################################################################
counter_instruction = 0
counter  = 0

while counter < counter_order - 1:

    instruction = root_program[counter]

######################################## ADD #######################################š###########

    if instruction.attrib["opcode"] == "ADD":

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

        elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
            var1 = getVar(instruction[1].text) # 0. - typ      1. - hodnota
            var2 = getVar(instruction[2].text) # 0. - typ      1. - hodnota
            if var1[0] == "int" and var2[0] == "int":
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
############################################# SUB ##############################################
    elif instruction.attrib["opcode"] == "SUB":

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
            if var1[0] == "int" and var2[0] == "int":
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
########################################### MUL ##################################################
    elif instruction.attrib["opcode"] == "MUL":

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
            if var1[0] == "int" and var2[0] == "int":
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
######################################## IDIV #################################################
    elif instruction.attrib["opcode"] == "IDIV":

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
####################################### LT GT EQ ###################################################
    elif instruction.attrib["opcode"] in ["LT","GT","EQ"]:
            if instruction[1].attrib["type"] != instruction[2].attrib["type"]:
                errorMessage("nekopatibilne typy",32)
            else:
######################################    LT GT  ############################################################
                if instruction.attrib["opcode"] in ["LT","GT"]:
                    if instruction[1].attrib["type"] == "nil" or instruction[2].attrib["type"] == "nil":
                        errorMessage("nemozno porovnavat pri LT a EQ nil",53)
                    else:
########################################### LT ###############################################################
                        if instruction.attrib["opcode"] == "LT":

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

################################################### GT #####################################################
                        elif instruction.attrib["opcode"] == "GT":

                            if instruction[1].attrib["type"] == "var":
                                var = getVar(instruction[1].text)
                                result = var[1] > instruction[2].text
                                identifFrame(instruction[0].text,"bool",result)
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

############################################### EQ ##########################################################
                elif instruction.attrib["opcode"] == "EQ":

                    if instruction[1].attrib["type"] == "var":
                        var = getVar(instruction[1].text)
                        result = var[1] == instruction[2].text
                        identifFrame(instruction[0].text,"bool",result)
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
########################################š EQ pre NIL #####################################################š
            if instruction.attrib["opcode"] == "EQ":
                if instruction[1].attrib["type"] == "nil" or instruction[2].attrib["type"] == "nil":
                    if instruction[1].attrib["type"] == "var":
                        var = getVar(instruction[1].text)
                        result = var[1] == instruction[2].text
                        identifFrame(instruction[0].text,"bool",result)
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

############################################ AND #################################################
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
############################################### OR ###########################################################
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
####################################### NOT ################################################
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
################################ INT2CHAR ######################################################
    elif instruction.attrib["opcode"] == "INT2CHAR":
        if instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "int":
                var[1] = int(var[1])
                try:
                    result = chr(var[1])
                    identifFrame(instruction[0].text,"string",result)
                except ValueError as error:
                    errorMessage(error.args[0],58)
            else:
                errorMessage("nejaka chyba nejaky navratovy kod neviem aky",32)
        elif instruction[1].attrib["type"] == "int":
            value = int(instruction[1].text)
            try:
                result = chr(value)
                identifFrame(instruction[0].text,"string",result)
            except ValueError as error:
                errorMessage(error.args[0],58)
        else:
            errorMessage("zle zle zle",32)
####################################### STRI2INT #################################################š
    elif instruction.attrib["opcode"] == "STRI2INT":

        if instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "string" and instruction[2].attrib["type"] == "int":

                var[1] = replaceEscapeSeq(var[1])
                intValue = int(instruction[2].text)
                if 0 <= intValue < len(var[1]):
                    ordasci = [ord(c) for c in var[1]]
                    result = ordasci[intValue]
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("Mimo rozsah u STRI2INT",58)
            else:
                errorMessage("Zle zadane typy pri STRI2INT",32)
        elif instruction[2].attrib["type"] == "var":
            var = getVar(instruction[2].text)
            if var[0] == "string" and instruction[1].attrib["type"] == "int":

                var[1] = replaceEscapeSeq(var[1])
                intValue = int(instruction[1].text)
                if 0 <= intValue < len(var[1]):
                    ordasci = [ord(c) for c in var[1]]
                    result = ordasci[intValue]
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("Mimo rozsah u STRI2INT",58)
            else:
                errorMessage("Zle zadane typy pri STRI2INT",32)
        elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            var2 = getVar(instruction[2].text)
            if var[0] == "string" and var2[0] == "int":

                
                var[1] = replaceEscapeSeq(var[1])
                if 0 <= var2[1] < len(var[1]):
                    ordasci = [ord(c) for c in var[1]]
                    result = ordasci[var2[1]]
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("Mimo rozsah u STRI2INT",58)
            else:
                errorMessage("Zle zadane typy pri STRI2INT",32)
        else:
            if instruction[1].attrib["type"] == "string" and instruction[2].attrib["type"] == "int":
                stringValue = instruction[1].text
                stringValue = replaceEscapeSeq(instruction[1].text)
                intValue = int(instruction[2].text)
                if 0 <= intValue < len(stringValue):
                    ordasci = [ord(c) for c in stringValue]
                    result = ordasci[intValue]
                    identifFrame(instruction[0].text,"int",result)
                else:
                    errorMessage("Mimo rozsah u STR2INT",58)
            else:
                errorMessage("Zle zadane typy pri STRI2INT",32)
#################################### EXIT ###################################################
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
#################################### CONCAT ###################################################
    elif instruction.attrib["opcode"] == "CONCAT": # <var> <symb1> <symb2>
        if instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "string" and instruction[2].attrib["type"] == "string":
                var[1] = replaceEscapeSeq(var[1])
                result = var[1] + instruction[2].text
                identifFrame(instruction[0].text,"string",result)
            else:
                errorMessage("ERROR",32)
        elif instruction[2].attrib["type"] == "var":
            var = getVar(instruction[2].text)
            if var[0] == "string" and instruction[1].attrib["type"] == "string":
                var[1] = replaceEscapeSeq(var[1])
                result = var[1] + instruction[1].text
                identifFrame(instruction[0].text,"string",result)
            else:
                errorMessage("ERROR",32)
        elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
            var1 = getVar(instruction[1].text)
            var2 = getVar(instruction[2].text)
            if var1[0] == "string" and var2[0] == "string":
                var1[1] = replaceEscapeSeq(var1[1])
                var2[1] = replaceEscapeSeq(var2[1])
                result = var1[1] + var2[1]
                identifFrame(instruction[0].text,"string",result)
            else:
                errorMessage("ERROR",32)
        else:
              if instruction[1].attrib["type"] != "string" or instruction[2].attrib["type"] != "string":
                  errorMessage("pri CONCAT musi byt symb1 aj symb2 type: string",32)
              else:
                 symb1 = replaceEscapeSeq(instruction[1].text)
                 symb2 = replaceEscapeSeq(instruction[2].text)
                 result = symb1 + symb2
                 identifFrame(instruction[0].text,"string",result)
########################################### STRLEN ############################################
    elif instruction.attrib["opcode"] == "STRLEN":
        if instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "string":
                var[1] = replaceEscapeSeq(var[1])
                result = int(len(var[1]))
                identifFrame(instruction[0].text,"int",result)
            else:
                errorMessage("Error",32)
        elif instruction[1].attrib["type"] == "string":
            symb1 = replaceEscapeSeq(instruction[1].text)
            result = int(len(symb1))
            identifFrame(instruction[0].text,"int",result)
        else:
            errorMessage("eer",32)
####################################### GETCHAR #############################################
    elif instruction.attrib["opcode"] == "GETCHAR":
        if instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "string" and instruction[2].attrib["type"] == "int":
                var[1] = replaceEscapeSeq(var[1])
                intValue = int(instruction[2].text) #int hodnota
                if 0 <= intValue < len(var[1]):
                    listStringvalue = list(var[1])
                    result = listStringvalue[intValue]
                    identifFrame(instruction[0].text,"string",result)
                else:
                    errorMessage("Mimo rozsah u GETCHAR",58)
            else:
                errorMessage("chyba",32)
        elif  instruction[2].attrib["type"] == "var":
            var = getVar(instruction[2].text)
            if var[0] == "string" and instruction[1].attrib["type"] == "int":
                var[1] = replaceEscapeSeq(var[1])
                intValue = int(instruction[1].text) #int hodnota
                if 0 <= intValue < len(var[1]):
                    listStringvalue = list(var[1])
                    result = listStringvalue[intValue]
                    identifFrame(instruction[0].text,"string",result)
                else:
                    errorMessage("Mimo rozsah u GETCHAR",58)
            else:
                errorMessage("chyba",32)
        elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
            var1 = getVar(instruction[1].text)
            var2 = getVar(instruction[2].text)
            if var1[0] == "string" and var2[0] == "int":

                var1[1] = replaceEscapeSeq(var1[1])

                if 0 <= var2[1] < len(var1[1]):
                    listStringvalue = list(var1[1])
                    result = listStringvalue[var2[1]]
                    identifFrame(instruction[0].text,"string",result)
                else:
                    errorMessage("Mimo rozsah u GETCHAR",58)
            else:
                errorMessage("chyba",32)
        else:
            if instruction[1].attrib["type"] == "string" and instruction[2].attrib["type"] == "int":
                stringValue = instruction[1].text
                stringValue = replaceEscapeSeq(instruction[1].text)
                intValue = int(instruction[2].text)
                if 0 <= intValue < len(stringValue):
                    listStringvalue = list(stringValue)
                    result = listStringvalue[intValue]
                    identifFrame(instruction[0].text,"string",result)
                else:
                    errorMessage("Mimo rozsah u GETCHAR",58)
            else:
                 errorMessage("zle zadane typy pri GETCHAR, symb1 ma byt string, symb2 : int",32)
########################################## SETCHAR #############################################
    elif instruction.attrib["opcode"] == "SETCHAR":
        if instruction[0].attrib["type"] == "var" and instruction[1].attrib["type"] == "var":
            string = getVar(instruction[0].text)
            index = getVar(instruction[1].text)
            char = instruction[2].text
            if string[0] == "string" and index[0] == "int" and char == "string":
                string[1] = replaceEscapeSeq(string[1])
                char = replaceEscapeSeq(instruction[2].text)
                if 0 <= index[1] < len(string[1]):
                    if char != "":
                        result = string[1][:index[1]] + char[0] + string[1][index[1] +1:]  #orezeme podla indexu cize ked mame ahoj a idndex bude 2 tak bude ah pridame 0znak napr a cize aha a plus to co tam bolo
                        identifFrame(instruction[0].text,"string",result)
                    else:
                        errorMessage("Pradny retazec symb2 u SETCHAR",58)
                else:
                    errorMessage("Mimo rozsah u SETCHAR",58)

            else:
                errorMessage("pojeb",32)
        elif instruction[0].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
            string = getVar(instruction[0].text)
            char = getVar(instruction[2].text)
            index = int(instruction[1].text)
            if string[0] == "string" and index == "int" and char[0] == "string":
                string[1] = replaceEscapeSeq(string[1])
                char[1] = replaceEscapeSeq(char[1])
                if 0 <= index < len(string[1]):
                    if char[1] != "":
                        result = string[1][:index] + char[1][0] + string[1][index + 1:]
                        identifFrame(instruction[0].text,"string",result)
                    else:
                        errorMessage("Pradny retazec symb2 u SETCHAR",58)
                else:
                    errorMessage("Mimo rozsah u SETCHAR",58)

            else:
                errorMessage("pojeb",32)
        elif instruction[0].attrib["type"] == "var" and instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
            string = getVar(instruction[0].text)
            index = getVar(instruction[1].text)
            char = getVar(instruction[2].text)
            if string[0] == "string" and index[0] == "int" and char[0] == "string":

                string[1] = replaceEscapeSeq(string[1])
                char[1] = replaceEscapeSeq(char[1])
                if 0 <= index[1] < len(string[1]):
                    if char[1] != "":
                        result = string[1][:index[1]] + char[1][0] + string[1][index[1] + 1:]
                        identifFrame(instruction[0].text,"string",result)
                    else:
                        errorMessage("Pradny retazec symb2 u SETCHAR",58)
                else:
                    errorMessage("Mimo rozsah u SETCHAR",58)
            else:
                errorMessage("aaa",32)

        else:
            if instruction[0].attrib["type"] == "var" and instruction[1].attrib["type"] == "int" and instruction[2].attrib["type"] == "string":
                string = getVar(instruction[0].text)
                if string[0] == "string":

                    index = int(instruction[1].text)
                    char = instruction[2].text
                    string[1] = replaceEscapeSeq(string[1])
                    char = replaceEscapeSeq(instruction[2].text)
                    if 0 <= index < len(string[1]):
                        if char != "":
                            result = string[1][:index] + char[0] + string[1][index + 1:]
                            identifFrame(instruction[0].text,"string",result)
                        else:
                            errorMessage("Pradny retazec symb2 u SETCHAR",58)
                    else:
                        errorMessage("Mimo rozsah u SETCHAR",58)
            else:
                 errorMessage("zle zadane typy pri SETCHAR, symb1 ma byt int, symb2 : string",32)
######################################## TYPE ###############################################################
    elif instruction.attrib["opcode"] == "TYPE": # <var> <symb>

        if instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text) # symb = var
            if var[0] == "int":
                identifFrame(instruction[0].text,"string","int")
            elif var[0] == "string":
                var[1] = replaceEscapeSeq(var[1])
                identifFrame(instruction[0].text,"string","string")
            elif var[0] == "bool":
                identifFrame(instruction[0].text,"string","bool")
            elif var[0] == "nil":
                identifFrame(instruction[0].text,"string","nil")
            else:
                errorMessage("aa",32)
        else:

            if instruction[1].attrib["type"] == "int":
                identifFrame(instruction[0].text,"string","int")
            elif instruction[1].attrib["type"] == "string":
                instruction[1].text = replaceEscapeSeq(instruction[1].text)
                identifFrame(instruction[0].text,"string","string")
            elif instruction[1].attrib["type"] == "bool":
                identifFrame(instruction[0].text,"string","bool")
            elif instruction[1].attrib["type"] == "nil":
                identifFrame(instruction[0].text,"string","nil")
            else:
                errorMessage("zle typt",32)


################################################ DPRINT ###########################################################
    elif instruction.attrib["opcode"] == "DPRINT":

        if instruction[0].attrib["type"] == "string":
            instruction[0].text = replaceEscapeSeq(instruction[0].text)
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
################################################# BREAK ##########################################################
    elif instruction.attrib["opcode"] == "BREAK":
        sys.stderr.write("\nPozicia kodu:{0} \n".format(instruction.attrib["order"]))
        sys.stderr.write("Labels:{0}\n".format(Labels))
        sys.stderr.write("Obsah LF:{0}\n".format(LF))
        sys.stderr.write("Obsah TF:{0}\n".format(TF))
        sys.stderr.write("Obsah GF:{0}\n".format(GF))
        sys.stderr.write("Pocet vykonanych instrukci:{0}\n".format(counter_instruction))
        sys.stderr.write("Zasobnik volani:{0}\n".format(callStack))
        sys.stderr.write("Zasobnik variable:{0}\n".format(dataStack))


#################################### MOVE ################################################################
    elif instruction.attrib["opcode"] == "MOVE": #<var> <symb> | moze byt var [int,string,bool,nil] alebo var var
        if instruction[1].attrib["type"] == "var": #ak je symb var
            var = getVar(instruction[1].text)
            if var[0] == "string":
                var[1] = replaceEscapeSeq(var[1])
            identifFrame(instruction[0].text,var[0],var[1])
        elif instruction[1].attrib["type"] in ["int","string","bool","nil"]:
            if instruction[1].attrib["type"] == "string":
                instruction[1].text = replaceEscapeSeq(instruction[1].text)
            identifFrame(instruction[0].text,instruction[1].attrib["type"],instruction[1].text)

        else:
            errorMessage("zle zle zle",32)
#################################### CREATEFRAME #################################################################
    elif instruction.attrib["opcode"] == "CREATEFRAME":

        TF = {}

################################################ PUSHFRAME ######################################################
    elif instruction.attrib["opcode"] == "PUSHFRAME":
        LF.append(TF)
        TF = None

############################################## POPFRAME ##############################################################
    elif instruction.attrib["opcode"] == "POPFRAME":
        try:
            TF = LF.pop()
        except IndexError as err:
            errorMessage(err.args[0],55)
#################################################### DEFVAR ################################################################
    elif instruction.attrib["opcode"] == "DEFVAR":
        variable = instruction[0].text.split("@",1)[1]
        frame = instruction[0].text.split("@",1)[0]
        if frame == "GF":
            GF[variable] = None
        if frame == "TF":
            if TF == None:
                errorMessage("Pristup k nedefinovanemu ramcu",55)
            else:
                TF[variable] = None
        if frame == "LF":
            if LF:
                print("hori mi rit")
                LF[-1][variable] = None
            else:
                errorMessage("Pristup k nedefinovanemu ramcu",55)
######################################################## CALL #####################################################
    elif instruction.attrib["opcode"] == "CALL":

        if instruction[0].text not in Labels:
            errorMessage("undefined label",52)
        else:
            callStack.append(counter + 1)
            counter = Labels.get(instruction[0].text)
            continue # preto aby sme skocili hore do cyklu a nepokracovali dalej

######################################################## RETURN ####################################################
    elif instruction.attrib["opcode"] == "RETURN":
        try:
            counter = callStack.pop()
        except IndexError as err:
            errorMessage(err.args[0],55)
        continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
###################################### JUMP ###########################################################
    elif instruction.attrib["opcode"] == "JUMP":
        if instruction[0].text not in Labels:
            errorMessage("undefined label",52)
        else:
            counter = Labels.get(instruction[0].text)
            continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
####################################### JUMPIFEQ <label> <symb1> <symb2> ###############################################
    elif instruction.attrib["opcode"] == "JUMPIFEQ":
        if instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text) # symb1 = var
            if var[0] == instruction[2].attrib["type"] and var[1] == instruction[2].text:
                if var[0] == "string":
                    var[1] = replaceEscapeSeq(var[1])
                if instruction[0].text not in Labels:
                    errorMessage("undefined label",52)
                else:
                    counter = Labels.get(instruction[0].text)
                    continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
            else:
                errorMessage("ERROR JUMPIFEQ",53)

        elif instruction[2].attrib["type"] == "var":
            var = getVar(instruction[2].text) # symb2 = var
            if var[0] == instruction[1].attrib["type"] and var[1] == instruction[1].text:
                if var[0] == "string":
                    var[1] = replaceEscapeSeq(var[1])
                if instruction[0].text not in Labels:
                    errorMessage("undefined label",52)
                else:
                    counter = Labels.get(instruction[0].text)
                    continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
            else:
                errorMessage("ERROR JUMPIFEQ",53)
        elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
            var1 = getVar(instruction[1].text) # symb1 = var
            var2 = getVar(instruction[2].text) # symb2 = var
            if var1[0] == var2[0] and va1r[1] == var2[1]:
                if var1[0] == "string":
                    var1[1] = replaceEscapeSeq(var1[1])
                elif var2[0] == "string":
                    var2[1] = replaceEscapeSeq(var2[1])
                if instruction[0].text not in Labels:
                    errorMessage("undefined label",52)
                else:
                    counter = Labels.get(instruction[0].text)
                    continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
            else:
                errorMessage("ERROR JUMPIFEQ",53)
        else:
            if instruction[1].attrib["type"] == instruction[2].attrib["type"] and instruction[1].text == instruction[2].text:
                if instruction[1].attrib["type"] == "string":
                    instruction[1].text = replaceEscapeSeq(instruction[1].text)
                elif instruction[2].attrib["type"] == "string":
                    instruction[2].text = replaceEscapeSeq(instruction[2].text)
                if instruction[0].text not in Labels:
                    errorMessage("undefined label",52)
                else:
                    counter = Labels.get(instruction[0].text)
                    continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
            else:
                errorMessage("ERROR JUMPIFEQ",53)
############################################### JUMPIFNEQ ########################################################
    elif instruction.attrib["opcode"] == "JUMPIFNEQ":
         if instruction[1].attrib["type"] == "var":
             var = getVar(instruction[1].text) # symb1 = var
             if var[0] == instruction[2].attrib["type"] and var[1] != instruction[2].text:
                 if var[0] == "string":
                     var[1] = replaceEscapeSeq(var[1])
                 if instruction[0].text not in Labels:
                     errorMessage("undefined label",52)
                 else:
                     counter = Labels.get(instruction[0].text)
                     continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
             else:
                 errorMessage("ERROR JUMPIFNEQ",53)

         elif instruction[2].attrib["type"] == "var":
             var = getVar(instruction[2].text) # symb2 = var
             if var[0] == instruction[1].attrib["type"] and var[1] != instruction[1].text:
                 if var[0] == "string":
                     var[1] = replaceEscapeSeq(var[1])
                 if instruction[0].text not in Labels:
                     errorMessage("undefined label",52)
                 else:
                     counter = Labels.get(instruction[0].text)
                     continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
             else:
                 errorMessage("ERROR JUMPIFNEQ",53)
         elif instruction[1].attrib["type"] == "var" and instruction[2].attrib["type"] == "var":
             var1 = getVar(instruction[1].text) # symb1 = var
             var2 = getVar(instruction[2].text) # symb2 = var
             if var1[0] == var2[0] and va1r[1] != var2[1]:
                 if var1[0] == "string":
                     var1[1] = replaceEscapeSeq(var1[1])
                 elif var2[0] == "string":
                     var2[1] = replaceEscapeSeq(var2[1])
                 if instruction[0].text not in Labels:
                     errorMessage("undefined label",52)
                 else:
                     counter = Labels.get(instruction[0].text)
                     continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
             else:
                 errorMessage("ERROR JUMPIFNEQ",53)
         else:
             if instruction[1].attrib["type"] == instruction[2].attrib["type"] and instruction[1].text != instruction[2].text:
                 if instruction[1].attrib["type"] == "string":
                     instruction[1].text = replaceEscapeSeq(instruction[1].text)
                 elif instruction[2].attrib["type"] == "string":
                     instruction[2].text = replaceEscapeSeq(instruction[2].text)
                 if instruction[0].text not in Labels:
                     errorMessage("undefined label",52)
                 else:
                     counter = Labels.get(instruction[0].text)
                     continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
             else:
                 errorMessage("ERROR JUMPIFNEQ",53)

######################################################## PUSHS #####################################################
    elif instruction.attrib["opcode"] == "PUSHS":
        if instruction[0].attrib["type"] == "var":
            var = getVar(instruction[0].text)
            var[1] = replaceEscapeSeq(var[1])
            dataStack.append(var)
        else:
            dataStack.append([instruction[0].attrib["type"],instruction[0].text])
########################################################## POPS ####################################################
    elif instruction.attrib["opcode"] == "POPS": # TODO
        if instruction[0].attrib["type"] == "var":
            var = getVar(instruction[0].text)
            if var[0] == "string":
                var[1] = replaceEscapeSeq(var[1])
            try:
                var = dataStack.pop()
            except IndexError as err:
                errorMessage(err.args[0],56)
            identifFrame(instruction[0].text,var[0],var[1])
        else:
            errorMessage("zly typ",32)
############################################ READ ##################################################################
    elif instruction.attrib["opcode"] == "READ": #var type
        if STDINInput: #ak je STDIN input true
            inputl = input()
        else:
            inputl = input.readline().split("\n")[0]
        check_typebool = re.search("^true",inputl,re.IGNORECASE) #regulak pre bool hlada true a je jedno ci True alebo true alebo TRUE
        check_typestring = re.search("([^\ \\\\#]|\\\\[0-9]{3})*$",inputl)
        check_typeint = re.search("^((\+|-)?[0-9]\d*)$",inputl)


        if instruction[1].text == "int":
            if check_typeint:
                inputInteger = int(inputl)
                identifFrame(instruction[0].text,"int",inputInteger)
            else:
                inputInteger = 0
                identifFrame(instruction[0].text,"int",inputInteger)

        elif instruction[1].text == "string":
            if check_typestring:
                inputString = inputl
                inputString = replaceEscapeSeq(inputString)
                identifFrame(instruction[0].text,"string",inputString)
            else:
                inputString = ""
                identifFrame(instruction[0].text,"string",inputString)
        elif instruction[1].text == "bool":
            if check_typebool:
                inputBool = "true"
                identifFrame(instruction[0].text,"bool",inputBool)
            else:
                inputBool = "false"
                identifFrame(instruction[0].text,"bool",inputBool)

        else:
            errorMessage("zle zadany typ",32)
######################################### WRITE #################################################
    elif instruction.attrib["opcode"] == "WRITE":  #<symb>
        if instruction[0].attrib["type"] == "bool":
            if instruction[0].text == "true":
                print("true",end='')
            else:
                print("false",end='')
        elif instruction[0].attrib["type"] == "int":
            print(int(instruction[0].text),end='')
        elif instruction[0].attrib["type"] == "string":
            instruction[0].text = replaceEscapeSeq(instruction[0].text)
            print(instruction[0].text,end='')
        elif instruction[0].attrib["type"] == "var":
            var = getVar(instruction[0].text)

            if var[0] == "int":
                print(int(var[1]),end='')
            elif var[0] == "string":
                var[1] = replaceEscapeSeq(var[1])
                print(var[1],end ='')
            elif var[0] == "bool":
                if var[1] == "true":
                    print("true",end='')
                else:
                    print("false",end='')
            elif var[0] == "nil":
                print(var[1],end='')
            else:
                errorMessage("spatny typ",32)
        elif instruction[0].attrib["type"] == "nil":
            print(instruction[0].text, end='')
        else:
            errorMessage("Zly typ",32)



    counter += 1
    counter_instruction += 1
#dom.write("example.xml")
