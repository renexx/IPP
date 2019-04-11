#!/usr/bin/env python3
#
# Project: Project for Principles of Programming Languages subject
# @file interpret.php
# autor René Bolf xbolfr00@stud.fit.vutbr.cz
import sys
import xml.etree.ElementTree as ElementTree # for XML
import re # for regular expression


def errorMessage(message,exitCode):
    """ This function is for processing error code and errorMessage"""
    print("ERR: " + message + "\n", file = sys.stderr)
    sys.exit(exitCode)

def showHelp():
    """ This function is for printing help"""
     print("""
      **********************************HELP************************************************************************************************************************************************
      HELP : --help print help
      This script load XML program representation from specified file and interprets the program using standart input and standart output
      Input XMl is from parse.php but no necessarily from source code in IPPCODE19
     ******************************HOW TO RUN *********************************************************************************************************************************************
     --help - print help
     --source=file input file with XML representation of source code according to specification
     --input=file file with input for interpretation specified source code
     --parse-script=file - file with script in PHP7.3 for analysis source code in IPPcode19(if this parameter is missing, so implicity vaulue is parse.php (in acutal direcotry))
     """)
     sys.exit(0)

STDINInput = False
########################### CHECKING ARGUMENTS ############################################################
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
############################# LOADING XML ###################################################################################
try:
    dom = ElementTree.parse(argv_source) #object
except OSError as error:
    errorMessage(error.args[1],11) # except when open files
except ElementTree.ParseError as error:
    errorMessage(error.args[0],31) #when is no  well formated

root_program = dom.getroot()#root program
################################# CHECKING XML ########################################################################
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
    """ FUnction for check symbol [int,string,nil,bool,var]"""
    if(attribType == "int"):
        check_symbolint = re.search("^((\+|-)?[0-9]\d*)$",operand)
        if not check_symbolint:
            errorMessage("Wrong entered type: int",32)
    elif(attribType == "string"):
        if not operand:
            return
        check_symbolstring = re.search("^([^\ \\\\#]|\\\\[0-9]{3})*$",operand)
        if not check_symbolstring:
            errorMessage("Wrong entered type: string",32)
    elif(attribType == "bool"):
        check_symbolbool = re.search("^(true|false)$",operand)
        if not check_symbolbool:
            errorMessage("Wrong entered type: bool",32)
    elif(attribType == "nil"):
        check_symbolnil =  re.search("^nil$",operand)
        if not check_symbolnil:
            errorMessage("Wrong entered type: nil",32)
    elif(attribType == "var"):
        check_var = re.search("^(LF|GF|TF)@([a-zA-Z]|[_|\-|\$|&|%|\?|\!|\*])([a-zA-Z]|[0-9]|[_|\-|\$|&|%|\?|\!|\*])*$",operand)
        if not check_var:
            errorMessage("Wrong entered type: var",32)
    else:
        errorMessage("Wrong symbol",32)

def variableCheck(attribType,operand):
""" FUnction for check variable [var]"""
    if(attribType == "var"):
        check_var = re.search("^(LF|GF|TF)@([a-zA-Z]|[_|\-|\$|&|%|\?|\!|\*])([a-zA-Z]|[0-9]|[_|\-|\$|&|%|\?|\!|\*])*$",operand)
        if not check_var:
            errorMessage("Wrong entered type: var",32)

def labelCheck(attribType,operand):
    """ FUnction for check label [label]"""
    if(attribType == "label"):
        check_label = re.search("^([a-zA-Z]|[_|\-|\$|&|%|\?|\!|\*])([a-zA-Z]|[0-9]|[_|\-|\$|&|%|\?|\!|\*])*$",operand)
        if not check_label:
            errorMessage("Wrong entered type: label",32)

def typeCheck(attribType,operand):
    """ FUnction for check type [int,string,bool]"""
    if(attribType == "type"):
        check_type = re.search("^(int|string|bool)$",operand)
        if not check_type:
            errorMessage("Wrong entered type: type",32)



#Check ELEMENT instruction  [opcode a order]
for instruction in root_program:
    if(instruction.tag != "instruction"):
        errorMessage("Missing instruction element",32)

    if(len(instruction.attrib) != 2):
        errorMessage("Wrong count of operands",32)
    else:
        if "order" not in instruction.attrib or "opcode" not in instruction.attrib:
            errorMessage("Missing order or opcode",32)
###################################################################################
#Check specified opcode [Lexical,Syntaktic]
# 0 operandov CREATEFRAME PUSHFRAME POPFRAME RETURN break
    if instruction.attrib["opcode"] in ["CREATEFRAME","PUSHFRAME","POPFRAME","RETURN","BREAK"]: #something like switch
        for argument in instruction:
            if len(argument) != 0:
                errorMessage("Argument has an element",32)
            if len(argument.attrib) != 1:
                errorMessage("Bad attribute",32)
            if(argument.tag != 0):
                errorMessage("Wrong count of arguments in instruction: CREATEFRAME,PUSHFRAME,POPFRAME,RETURN,BREAK",32)
###################################################################################################################
# 1 operand  [var]  DEFVAR, POPS
    elif instruction.attrib["opcode"].upper() in ["DEFVAR","POPS"]:
        counter_arg = 0
        for argument in instruction:
            if len(argument) != 0:
                errorMessage("Argument has an element",32)
            if len(argument.attrib) != 1:
                errorMessage("Bad attribute",32)
            if "type" not in argument.attrib:
                errorMessage("Missing type in instruction: DEFVAR,POPS",32)
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "var"):
                    errorMessage("Instructions DEFVAR and POPS have to be type var",32)
                else:
                    variableCheck(argument.attrib["type"],argument.text)
            else:
                errorMessage("Wrong argument in instruction DEFVAR,POPS",32)
            counter_arg += 1
        if(counter_arg != 1):
            errorMessage("Wrong count of arguments in instruction DEFVAR,POPS",32)

# 1 operand [symb] = int, string, bool, nil PUSHS, WRITE,EXIT,DPRINT
    elif instruction.attrib["opcode"].upper() in ["PUSHS","WRITE","EXIT","DPRINT"]:
        counter_arg = 0
        for argument in instruction:
            if len(argument) != 0:
                errorMessage("Argument has an element",32)
            if len(argument.attrib) != 1:
                errorMessage("Bad attribute",32)
            if "type" not in argument.attrib:
                errorMessage("Missing type in instruction: PUSHS, WRITE ,EXIT,DPRINT",32)
            if(argument.tag == "arg1"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("In instruction PUSHS, WRITE, EXIT a DPRINT must be int, string, bool,nil or var ",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)
            else:
                errorMessage("Wrong argument in instruction: PUSHS, WRITE ,EXIT,DPRINT",32)
            counter_arg += 1
        if(counter_arg != 1):
            errorMessage("Wrong count of arguments in instructions: PUSH,WRITE,EXIT,DPRINT",32)

# 1 operand [label] CALL, LABEL, JUMP

    elif instruction.attrib["opcode"].upper() in ["CALL","LABEL","JUMP"]:
        counter_arg = 0
        for argument in instruction:
            if len(argument) != 0:
                errorMessage("Argument has an element",32)
            if len(argument.attrib) != 1:
                errorMessage("Bad attribute",32)
            if "type" not in argument.attrib:
                errorMessage("Missing type in instruction: CALL,LABEL,JUMP",32)
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "label"):
                    errorMessage("In instruction CALL, LABEL and JUMP must be label",32)
                else:
                    labelCheck(argument.attrib["type"],argument.text)
            else:
                errorMessage("Wrong argument in instruction: CALL LABEl A JUMP",32)
            counter_arg +=1
        if(counter_arg != 1):
            errorMessage("Wrong count of operands in instructions: CALL LABEL A JUMP",32)
# 2 operandy [var][symb]-int,string,bool,nil MOVE,INT2CHAR,TYPE,STRLEN
    elif instruction.attrib["opcode"].upper() in ["MOVE","INT2CHAR","TYPE","STRLEN","READ","NOT"]:
        counter_arg = 0
        for argument in instruction:
            if len(argument) != 0:
                errorMessage("Argument has an element",32)
            if len(argument.attrib) != 1:
                errorMessage("Bad attribute",32)
            if "type" not in argument.attrib:
                errorMessage("Chyba type u MOVE,INT2CHAR,TYPE,STRLEN,READ,NOT",32)
            counter_arg += 1
        if(counter_arg != 2):
            errorMessage("Zly pocet argumentov u MOVE,INT2CHAR,TYPE,STRLEN,READ,NOT",32)
#3 operandy [var] [symb1] [symb2] symbol moze byt var, int, string, bool, nil ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR
    elif instruction.attrib["opcode"].upper() in ["ADD","SUB","MUL","IDIV","LT","GT","EQ","AND","OR","STRI2INT","CONCAT","GETCHAR","SETCHAR","JUMPIFEQ","JUMPIFNEQ"]:
        counter_arg = 0
        for argument in instruction:
            if len(argument) != 0:
                errorMessage("Argument has an element",32)
            if len(argument.attrib) != 1:
                errorMessage("Bad attribute",32)
            if "type" not in argument.attrib:
                errorMessage("Missing type in instruction: ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR,JUMPIFEQ,JUMPIFNEQ",32)
            counter_arg += 1
        if(counter_arg != 3):
            errorMessage("Wrong count of  arguments in instruction: ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR,JUMPIFEQ,JUMPIFNEQ",32)
    else:
        errorMessage("Unknown operation code",32)

###################### SORTING XML (arg and order)#####################################################
root_program[:] = sorted(root_program, key=lambda child: int(child.get("order")))
for child in root_program:
    child[:] = sorted(child, key =lambda child: child.tag)

counter_order = 1
for instruction in root_program:
    if int(instruction.get("order")) != counter_order:
        errorMessage("Wrong order, order has to  started from 1",32)
# TOTO PRETO ABY NEBOLO PRI DAKEJ INSTRUKCI arg1 arg1##########################

    if instruction.attrib["opcode"].upper() in ["MOVE","INT2CHAR","TYPE","STRLEN","READ,NOT"]:
        if(instruction[0].tag != "arg1" or instruction[1].tag != "arg2"):
            errorMessage("Arguments are not in order in instruction: MOVE, INT2CHAR, TYPE, STRLEN, READ,NOT",32)
    if instruction.attrib["opcode"].upper() in ["ADD,SUB","MUL","IDIV","LT","GT","EQ","AND","OR","STRI2INT","CONCAT","GETCHAR","SETCHAR","JUMPIFEQ","JUMPIFNEQ"]:
        if(instruction[0].tag != "arg1" or instruction[1].tag != "arg2" or instruction[2].tag != "arg3"):
            errorMessage("Arguments are not in order in instruction:ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR,JUMPIFEQ,JUMPIFNEQ",32)

# 2 operandy [var][symb]-int,string,bool,nil MOVE,INT2CHAR,TYPE,STRLEN
    if instruction.attrib["opcode"].upper() in ["MOVE","INT2CHAR","TYPE","STRLEN","NOT"]:
        for argument in instruction:
            if len(argument) != 0:
                errorMessage("Argument has an element",32)
            if len(argument.attrib) != 1:
                errorMessage("Bad attribute",32)
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "var"):
                    errorMessage("In instruction MOVE,INT2CHAR,TYPE,STRLEN, NOT have to be arg1 var",32)
                else:
                    variableCheck(argument.attrib["type"],argument.text)
            elif(argument.tag == "arg2"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("In instruction MOVE,INT2CHAR,TYPE,STRLEN,NOT have to be arg2 int,string,bool,nil or var",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)
            else:
                errorMessage("Wrong arguments in instruction MOVE,INT2CHAR,TYPE,STRLEN,NOT",32)

# 2 operandy [var][type] READ
    elif instruction.attrib["opcode"].upper() in ["READ"]:
        for argument in instruction:
            if len(argument) != 0:
                errorMessage("Argument has an element",32)
            if len(argument.attrib) != 1:
                errorMessage("Bad attribute",32)
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "var"):
                    errorMessage("In instruction READ has to be arg1 var",32)
                else:
                    variableCheck(argument.attrib["type"],argument.text)
            elif(argument.tag == "arg2"):
                if(argument.attrib["type"] != "type"):
                    errorMessage("In instruction READ has to be arg2 type",32)
                else:
                    typeCheck(argument.attrib["type"],argument.text)
            else:
                errorMessage("Zle argumenty u READ",32)
#3 operandy [var] [symb1] [symb2] symbol moze byt var, int, string, bool, nil ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR
    elif instruction.attrib["opcode"].upper() in ["ADD","SUB","MUL","IDIV","LT","GT","EQ","AND","OR","STRI2INT","CONCAT","GETCHAR","SETCHAR"]:
        for argument in instruction:
            if len(argument) != 0:
                errorMessage("Argument has an element",32)
            if len(argument.attrib) != 1:
                errorMessage("Bad attribute",32)
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "var"):
                    errorMessage("In instruction: ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR has to be arg1: var",32)
                else:
                    variableCheck(argument.attrib["type"],argument.text)
            elif(argument.tag == "arg2"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("In instruction ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR has to be arg2: int,string,bool,nil,var",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)
            elif(argument.tag == "arg3"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("In instruction: ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR has to be arg3: int,string,bool,nil,var",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)
            else:
                errorMessage("Wrong arguments in instruction: ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,STRI2INT,CONCAT,GETCHAR,SETCHAR",32)
#3 oprandy [label] [symb1] [symb2]   JUMPIFEQ JUMPIFNEQ
    elif instruction.attrib["opcode"].upper() in ["JUMPIFEQ","JUMPIFNEQ"]:
        for argument in instruction:
            if len(argument) != 0:
                errorMessage("Argument has an element",32)
            if len(argument.attrib) != 1:
                errorMessage("Bad attribute",32)
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "label"):
                    errorMessage("In instruction JUMPIFEQ and JUMPIFNEQ has to be arg1 label",32)
                else:
                    labelCheck(argument.attrib["type"],argument.text)
            elif(argument.tag == "arg2"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("In instruction JUMPIFEQ and JUMPIFNEQ has to be arg2: int,string,bool,nil,var",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)
            elif(argument.tag == "arg3"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("In instruction JUMPIFEQ and JUMPIFNEQ has to be arg3: int,string,bool,nil,var",32)
                else:
                    symbolCheck(argument.attrib["type"],argument.text)
            else:
                errorMessage("Wrong count of arguments in instruction: JUMPIFEQ a JUMPIFNEQ",32)


    counter_order += 1


GF = {} # create dictionary for Global frame c
TF = None # temporary frame set to None value (is not defined)
LF = [] # list (stack) for local frame
dataStack = [] #stack for variable(data)
callStack = [] # stack for call label
Labels = {}

def identifFrame(variable,value,typ):
    """ FUnction for identifi frame [Global frame, temporary frame, local frame]"""
    frame = variable.split("@",1)[0] # split @ from variable
    variableName = variable.split("@",1)[1]
    if typ == "string":
        value = replaceEscapeSeq(value)
    if frame == "GF":
        if variableName not in GF:
            errorMessage("variable is not in global frame",54)
        else:
            GF[variableName] = [value,typ]
    if frame == "TF":
        if TF == None:
            errorMessage("Access to undefined temporary frame",55)
        elif variableName not in TF:
            errorMessage("variable is not in temporary frame",54)
        else:
            TF[variableName] = [value,typ]
    if frame == "LF":

        if LF:
            if variableName not in LF[-1]:
                errorMessage("variable is not in local frame",54)
            else:
                LF[-1][variableName] = [value,typ]
        else:
            errorMessage("Access to undefined local frame",55)

def getVar(variable):
    """ FUnction for getting variable from frame"""
    frame = variable.split("@",1)[0]
    variableName = variable.split("@",1)[1]
    if frame == "GF":
        if variableName not in GF:
            errorMessage("variable is not in global frame",54)
        elif GF.get(variableName) == None:
            errorMessage("variable uninitialized",56)
        else:
            return GF.get(variableName)
    if frame == "TF":
        if TF == None:
            errorMessage("Access to undefined temporary frame",55)
        elif variableName not in TF:
            errorMessage("variable is not in temporary frame",54)
        elif TF.get(variableName) == None:
            errorMessage("variable uninitialized",56)
        else:
            return TF.get(variableName)
    if frame == "LF":
        if LF:
            if variableName not in LF[-1]:
                errorMessage("variable is not in local frame",54)
            elif LF[-1].get(variableName) == None:
                errorMessage("variable uninitialized",56)
            else:
                return LF[-1].get(variableName)
        else:
            errorMessage("Access to undefined local frame",55)

def replaceEscapeSeq(string):
    """ FUnction for replacing escape seqvencies"""
    if not string:
        return ""
    string1 = re.findall("[0-9]{3}", string)

    for i in string1:
        string = string.replace("\\{0}".format(i) ,chr(int(i)))

    return string

for instruction in root_program:
######################################## LABEL #######################################################
        if instruction.attrib["opcode"].upper() == "LABEL":

            if instruction[0].text in Labels:
                errorMessage("Redefination of existing label",52)
            else:
                Labels[instruction[0].text] = int(instruction.attrib["order"])

###############################################################################################################
counter_instruction = 0
counter  = 0

while counter < counter_order - 1:

    instruction = root_program[counter]

######################################## ADD #######################################š###########

    if instruction.attrib["opcode"].upper() in ["ADD","SUB","MUL","IDIV"]:
        if instruction[1].attrib["type"] == "int":
            operand1 = int(instruction[1].text)

        elif instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "int":
                operand1 = int(var[1])
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)

        if instruction[2].attrib["type"] == "int":
            operand2 = int(instruction[2].text)

        elif instruction[2].attrib["type"] == "var":
            var = getVar(instruction[2].text)
            if var[0] == "int":
                operand2 = int(var[1])
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)

        if type(operand1) == type(operand2):
            if instruction.attrib["opcode"].upper() == "ADD":
                result = operand1 + operand2
                identifFrame(instruction[0].text,"int",result)

            elif instruction.attrib["opcode"].upper() == "SUB":
                result = operand1 - operand2
                identifFrame(instruction[0].text,"int",result)
            elif instruction.attrib["opcode"].upper() == "MUL":
                result = operand1 * operand2
                identifFrame(instruction[0].text,"int",result)
            elif instruction.attrib["opcode"].upper() == "IDIV":
                try:
                    result = operand1 // operand2
                except ZeroDivisionError as err:
                    errorMessage(err.args[0],57)
                identifFrame(instruction[0].text,"int",result)
        else:
            errorMessage("Wrong types",53)

####################################### LT GT EQ ###################################################

    elif instruction.attrib["opcode"].upper() in ["LT","GT"]:
######################################    LT GT  ############################################################
        if instruction[1].attrib["type"] == "int":
            operand1 = int(instruction[1].text)
        elif instruction[1].attrib["type"] == "bool":
            if instruction[1].text == "true":
                operand1 = True
            else:
                operand1 = False
        elif instruction[1].attrib["type"] == "string":
            operand1 = replaceEscapeSeq(instruction[1].text)
        elif instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "int":
                operand1 = int(var[1])
            elif var[0] == "bool":
                if var[1] == "true":
                    operand1 = True
                else:
                    operand1 = False
            elif var[0] == "string":
                operand1 = replaceEscapeSeq(var[1])
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)
        if instruction[2].attrib["type"] == "int":
            operand2 = int(instruction[2].text)
        elif instruction[2].attrib["type"] == "bool":
            if instruction[2].text == "true":
                operand2 = True
            else:
                operand2 = False
        elif instruction[2].attrib["type"] == "string":
            operand2 = replaceEscapeSeq(instruction[2].text)
        elif instruction[2].attrib["type"] == "var":
            var = getVar(instruction[2].text)
            if var[0] == "int":
                operand2 = int(var[1])
            elif var[0] == "bool":
                if var[1] == "true":
                    operand2 = True
                else:
                    operand2 = False
            elif var[0] == "string":
                operand2 = replaceEscapeSeq(var[1])
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)
        if type(operand1) == type(operand2):
            if instruction.attrib["opcode"].upper() == "LT":
                result = operand1 < operand2
                if result == True:
                    result = "true"
                else:
                    result = "false"
                identifFrame(instruction[0].text,"bool",result)
            elif instruction.attrib["opcode"].upper() == "GT":
                result = operand1 > operand2
                if result == True:
                    result = "true"
                else:
                    result = "false"
                identifFrame(instruction[0].text,"bool",result)
        else:
            errorMessage("Wrong types",53)

############################################### EQ ##########################################################
    elif instruction.attrib["opcode"].upper() == "EQ":
        if instruction[1].attrib["type"] == "int":
            operand1 = int(instruction[1].text)
        elif instruction[1].attrib["type"] == "bool":
            if instruction[1].text == "true":
                operand1 = True
            else:
                operand1 = False
        elif instruction[1].attrib["type"] == "string":
            operand1 = replaceEscapeSeq(instruction[1].text)
        elif instruction[1].attrib["type"] == "nil":
            operand1 = None
        elif instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "int":
                operand1 = int(var[1])
            elif var[0] == "bool":
                if var[1] == "true":
                    operand1 = True
                else:
                    operand1 = False
            elif var[0] == "nil":
                operand1 = None
            elif var[0] == "string":
                operand1 = replaceEscapeSeq(var[1])
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)
        if instruction[2].attrib["type"] == "int":
            operand2 = int(instruction[2].text)
        elif instruction[2].attrib["type"] == "bool":
            if instruction[2].text == "true":
                operand2 = True
            else:
                operand2 = False
        elif instruction[2].attrib["type"] == "string":
            operand2 = replaceEscapeSeq(instruction[2].text)
        elif instruction[2].attrib["type"] == "nil":
            operand2 = None
        elif instruction[2].attrib["type"] == "var":
            var = getVar(instruction[2].text)
            if var[0] == "int":
                operand2 = int(var[1])
            elif var[0] == "bool":
                if var[1] == "true":
                    operand2 = True
                else:
                    operand2 = False
            elif var[0] == "nil":
                operand2 = None
            elif var[0] == "string":
                operand2 = replaceEscapeSeq(var[1])
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)
        if type(operand1) != type(None) and type(operand2) != type(None):
            if type(operand1) != type(operand2):
                errorMessage("Wrong type",53)

            result = operand1 == operand2
            if result == True:
                result = "true"
            else:
                result = "false"
            identifFrame(instruction[0].text,"bool",result)
        else:
            result = operand1 == operand2
            if result == True:
                result = "true"
            else:
                result = "false"
            identifFrame(instruction[0].text,"bool",result)
############################################ AND  OR #################################################
    elif instruction.attrib["opcode"].upper() in ["AND","OR"]:
        if instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "bool":
                if var[1] == "true":
                    operand1 = True
                else:
                    operand1 = False
            else:
                errorMessage("Wrong types in AND or OR 676",53)
        elif instruction[1].attrib["type"] == "bool":
            if instruction[1].text == "true":
                operan1 = True
            else:
                operand1 = False
        else:
            errorMessage("wron types in AND or OR 683",53)
        if instruction[2].attrib["type"] == "var":
            var = getVar(instruction[2].text)
            if var[0] == "bool":
                if var[1] == "true":
                    operand2 = True
                else:
                    operand2 = False
            else:
                errorMessage("Wrong types in AND or OR 598",53)
        elif instruction[2].attrib["type"] == "bool":
            if instruction[2].text == "true":
                operan2 = True
            else:
                operand2 = False
        else:
            errorMessage("wron types in AND or OR 699",53)
        if type(operand1) == type(operand2):
            if instruction.attrib["opcode"].upper() == "AND":
                result = operand1 and operand2
                if result == True:
                    result = "true"
                else:
                    result = "false"
                identifFrame(instruction[0].text,"bool",result)
            elif instruction.attrib["opcode"].upper() == "OR":
                result = operand1 or operand2
                if result == True:
                    result = "true"
                else:
                    result = "false"
                identifFrame(instruction[0].text,"bool",result)
        else:
            errorMessage("Wrong types 716",53)


####################################### NOT ################################################
    elif instruction.attrib["opcode"].upper() == "NOT":
            if instruction[1].attrib["type"] == "var":
                var = getVar(instruction[1].text)
                if var[0] == "bool":
                    if var[1] == "true":
                        result = "false"
                    else:
                        result = "true"
                else:
                    errorMessage("Wrong types of operands in NOT",53)
            elif instruction[1].attrib["type"] == "bool":
                if instruction[1].text == "true":
                    result = "false"
                else:
                    result = "true"

            else:
                errorMessage("Wrong types of operands in NOT",53)
            identifFrame(instruction[0].text,"bool",result)

################################ INT2CHAR ######################################################
    elif instruction.attrib["opcode"].upper() == "INT2CHAR":
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
                errorMessage("Wrong types of operands in INT2CHAR",53)
        elif instruction[1].attrib["type"] == "int":
            value = int(instruction[1].text)
            try:
                result = chr(value)
                identifFrame(instruction[0].text,"string",result)
            except ValueError as error:
                errorMessage(error.args[0],58)
        else:
            errorMessage("Wrong types of operands in INT2CHAR",53)
####################################### STRI2INT #################################################š
    elif instruction.attrib["opcode"].upper() == "STRI2INT":

        if instruction[1].attrib["type"] == "string":
            stringValue = replaceEscapeSeq(instruction[1].text)

        elif instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "string":
                stringValue = replaceEscapeSeq(var[1])
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)

        if instruction[2].attrib["type"] == "int":
            intValue = int(instruction[2].text)

        elif instruction[2].attrib["type"] == "var":
            var = getVar(instruction[2].text)
            if var[0] == "int":
                intValue = int(var[1])
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)

        if 0 <= intValue < len(stringValue):
            ordasci = [ord(c) for c in stringValue]
            result = ordasci[intValue]
            identifFrame(instruction[0].text,"int",result)
        else:
            errorMessage("Out of range in STRI2INT",58)

#################################### EXIT ###################################################
    elif instruction.attrib["opcode"].upper() == "EXIT":
            if instruction[0].attrib["type"] == "int":
                exitInt = int(instruction[0].text)
            elif instruction[0].attrib["type"] == "var":
                var = getVar(instruction[0].text)
                if var[0] == "int":
                    exitInt = int(var[1])
                else:
                    errorMessage("Wrong type in EXIT",53)
            else:
                 errorMessage("EXIT: int or var",53)
            if 0 <= exitInt <= 49:
                sys.exit(exitInt)
            else:
                errorMessage("Spatna ciselna hodnota instrukcie EXIT",57)
#################################### CONCAT ###################################################
    elif instruction.attrib["opcode"].upper() == "CONCAT": # <var> <symb1> <symb2>
        if instruction[1].attrib["type"] == "string":
            operand1 = replaceEscapeSeq(instruction[1].text)

        elif instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "string":
                operand1 = replaceEscapeSeq(var[1])
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)

        if instruction[2].attrib["type"] == "string":
            operand2 = replaceEscapeSeq(instruction[2].text)

        elif instruction[2].attrib["type"] == "var":
            var = getVar(instruction[2].text)
            if var[0] == "string":
                operand2 = replaceEscapeSeq(var[1])
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)

        if type(operand1) == type(operand2):
            result = operand1 + operand2
            identifFrame(instruction[0].text,"string",result)

        else:
            errorMessage("Wrong types",53)


########################################### STRLEN ############################################
    elif instruction.attrib["opcode"].upper() == "STRLEN":
        if instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "string":
                var[1] = replaceEscapeSeq(var[1])
                result = int(len(var[1]))
                identifFrame(instruction[0].text,"int",result)
            else:
                errorMessage("Wrong type in STRLEN a",53)
        elif instruction[1].attrib["type"] == "string":
            symb1 = replaceEscapeSeq(instruction[1].text)
            result = int(len(symb1))
            identifFrame(instruction[0].text,"int",result)
        else:
            errorMessage("Wrong type in STRLEN b",53)
####################################### GETCHAR #############################################
    elif instruction.attrib["opcode"].upper() == "GETCHAR":

        if instruction[1].attrib["type"] == "string":
            stringValue = replaceEscapeSeq(instruction[1].text)

        elif instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "string":
                stringValue = replaceEscapeSeq(var[1])
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)

        if instruction[2].attrib["type"] == "int":
            intValue = int(instruction[2].text)

        elif instruction[2].attrib["type"] == "var":
            var = getVar(instruction[2].text)
            if var[0] == "int":
                intValue = int(var[1])
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)

        if 0 <= intValue < len(stringValue):
            listStringvalue = list(stringValue)
            result = listStringvalue[intValue]
            identifFrame(instruction[0].text,"string",result)
        else:
            errorMessage("Out of range in GETCHAR",58)

########################################## SETCHAR #############################################
    elif instruction.attrib["opcode"].upper() == "SETCHAR":

        if instruction[0].attrib["type"] == "var":
            stringVar = getVar(instruction[0].text)
            if stringVar[0] == "string":
                if stringVar[1] != "":
                    stringVar = replaceEscapeSeq(stringVar[1])
                else:
                    errorMessage("String in var is empty",58)
            else:
                errorMessage("Wrong types 836",53)
        else:
            errorMessage("Wrong types 838",53)

        if instruction[1].attrib["type"] == "int":
            index = int(instruction[1].text)
        elif instruction[1].attrib["type"] == "var":
            index = getVar(instruction[1].text)
            if index[0] == "int":
                index = int(index[1])
            else:
                errorMessage("Wrong types 846",53)
        else:
            errorMessage("Wrong types 848",53)

        if instruction[2].attrib["type"] == "string":
            if instruction[2].text != "":
                char = replaceEscapeSeq(instruction[2].text)
            else:
                errorMessage("String in symb2 is emepty",58)

        elif instruction[2].attrib["type"] == "var":
            char = getVar(instruction[2].text)
            if char[0] == "string":
                if char[1] != "":
                    char = replaceEscapeSeq(char[1])
                else:
                    errorMessage("String in var is empty",58)
            else:
                errorMessage("Wrong types 864",53)
        else:
            errorMessage("Wrong types 866",53)

        if 0 <= index < len(stringVar):
            result = stringVar[:index] + char[0] + stringVar[index + 1:]
            identifFrame(instruction[0].text,"string",result)
        else:
            errorMessage("Out of the bounds in SETCHAR",58)
######################################## TYPE ###############################################################
    elif instruction.attrib["opcode"].upper() == "TYPE": # <var> <symb>

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
                errorMessage("Wrong type in TYPE",53)
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
                errorMessage("Wrong type in TYPE",53)


################################################ DPRINT ###########################################################
    elif instruction.attrib["opcode"].upper() == "DPRINT":

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
    elif instruction.attrib["opcode"].upper() == "BREAK":
        sys.stderr.write("\nPozicia kodu:{0} \n".format(instruction.attrib["order"]))
        sys.stderr.write("Labels:{0}\n".format(Labels))
        sys.stderr.write("Obsah LF:{0}\n".format(LF))
        sys.stderr.write("Obsah TF:{0}\n".format(TF))
        sys.stderr.write("Obsah GF:{0}\n".format(GF))
        sys.stderr.write("Pocet vykonanych instrukci:{0}\n".format(counter_instruction))
        sys.stderr.write("Zasobnik volani:{0}\n".format(callStack))
        sys.stderr.write("Zasobnik variable:{0}\n".format(dataStack))


#################################### MOVE ################################################################
    elif instruction.attrib["opcode"].upper() == "MOVE": #<var> <symb> | can be var [int,string,bool,nil] or var var
        if instruction[1].attrib["type"] == "var": #if  symb is var
            var = getVar(instruction[1].text)
            if var[0] == "string":
                var[1] = replaceEscapeSeq(var[1])
            identifFrame(instruction[0].text,var[0],var[1])
        elif instruction[1].attrib["type"] in ["int","string","bool","nil"]:
            if instruction[1].attrib["type"] == "string":
                instruction[1].text = replaceEscapeSeq(instruction[1].text)
            identifFrame(instruction[0].text,instruction[1].attrib["type"],instruction[1].text)

        else:
            errorMessage("Wrong type in MOVE",53)
#################################### CREATEFRAME #################################################################
    elif instruction.attrib["opcode"].upper() == "CREATEFRAME":
        TF = {}
################################################ PUSHFRAME ######################################################
    elif instruction.attrib["opcode"].upper() == "PUSHFRAME":
        if TF == None:
            errorMessage("Access to undefined temporary frame",55)
        LF.append(TF)
        TF = None

############################################## POPFRAME ##############################################################
    elif instruction.attrib["opcode"].upper() == "POPFRAME":
        try:
            TF = LF.pop()
        except IndexError as err:
            errorMessage(err.args[0],55)
#################################################### DEFVAR ################################################################
    elif instruction.attrib["opcode"].upper() == "DEFVAR":
        variable = instruction[0].text.split("@",1)[1]
        frame = instruction[0].text.split("@",1)[0]
        if frame == "GF":
            GF[variable] = None
        if frame == "TF":
            if TF == None:
                errorMessage("Access to undefined temporary frame",55)
            else:
                TF[variable] = None
        if frame == "LF":
            if LF:
                LF[-1][variable] = None
            else:
                errorMessage("Access to undefined local frame",55)
######################################################## CALL #####################################################
    elif instruction.attrib["opcode"].upper() == "CALL":

        if instruction[0].text not in Labels:
            errorMessage("undefined label",52)
        else:
            callStack.append(counter + 1)
            counter = Labels.get(instruction[0].text)
            continue # preto aby sme skocili hore do cyklu a nepokracovali dalej

######################################################## RETURN ####################################################
    elif instruction.attrib["opcode"].upper() == "RETURN":
        try:
            counter = callStack.pop()
        except IndexError as err:
            errorMessage(err.args[0],56)
        continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
###################################### JUMP ###########################################################
    elif instruction.attrib["opcode"].upper() == "JUMP":
        if instruction[0].text not in Labels:
            errorMessage("undefined label",52)
        else:
            counter = Labels.get(instruction[0].text)
            continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
####################################### JUMPIFEQ <label> <symb1> <symb2> ###############################################
    elif instruction.attrib["opcode"].upper() in ["JUMPIFEQ","JUMPIFNEQ"]:
        if instruction[1].attrib["type"] == "int":
            operand1 = int(instruction[1].text)
        elif instruction[1].attrib["type"] == "bool":
            if instruction[1].text == "true":
                operand1 = True
            else:
                operand1 = False
        elif instruction[1].attrib["type"] == "string":
            operand1 = replaceEscapeSeq(instruction[1].text)
        elif instruction[1].attrib["type"] == "nil":
            operand1 = None
        elif instruction[1].attrib["type"] == "var":
            var = getVar(instruction[1].text)
            if var[0] == "int":
                operand1 = int(var[1])
            elif var[0] == "bool":
                if var[1] == "true":
                    operand1 = True
                else:
                    operand1 = False
            elif var[0] == "string":
                operand1 = replaceEscapeSeq(var[1])
            elif var[0] == "nil":
                operand1 = None
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)
        if instruction[2].attrib["type"] == "int":
            operand2 = int(instruction[2].text)
        elif instruction[2].attrib["type"] == "bool":
            if instruction[2].text == "true":
                operand2 = True
            else:
                operand2 = False
        elif instruction[2].attrib["type"] == "string":
            operand2 = replaceEscapeSeq(instruction[2].text)
        elif instruction[2].attrib["type"] == "nil":
            operand2 = None
        elif instruction[2].attrib["type"] == "var":
            var = getVar(instruction[2].text)
            if var[0] == "int":
                operand2 = int(var[1])
            elif var[0] == "bool":
                if var[1] == "true":
                    operand2 = True
                else:
                    operand2 = False
            elif var[0] == "string":
                operand2 = replaceEscapeSeq(var[1])
            elif var[0] == "nil":
                operand2 = None
            else:
                errorMessage("Wrong types",53)
        else:
            errorMessage("Wrong types",53)
        if type(operand1) == type(operand2):
            if instruction.attrib["opcode"].upper() == "JUMPIFEQ":
                result = operand1 == operand2
                if result:
                    if instruction[0].text not in Labels:
                        errorMessage("undefined label",52)
                    else:
                        counter = Labels.get(instruction[0].text)
                        continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
                        
            elif instruction.attrib["opcode"].upper() == "JUMPIFNEQ":
                result = not operand1 == operand2
                if result:
                    if instruction[0].text not in Labels:
                        errorMessage("undefined label",52)
                    else:
                        counter = Labels.get(instruction[0].text)
                        continue # preto aby sme skocili hore do cyklu a nepokracovali dalej
        else:
            errorMessage("Wrong types",53)


######################################################## PUSHS #####################################################
    elif instruction.attrib["opcode"].upper() == "PUSHS":
        if instruction[0].attrib["type"] == "var":
            var = getVar(instruction[0].text)
            var[1] = replaceEscapeSeq(var[1])
            dataStack.append(var)
        else:
            dataStack.append([instruction[0].attrib["type"],instruction[0].text])
########################################################## POPS ####################################################
    elif instruction.attrib["opcode"].upper() == "POPS": # TODO
        if instruction[0].attrib["type"] == "var":
            try:
                var = dataStack.pop()
            except IndexError as err:
                errorMessage(err.args[0],56)
            identifFrame(instruction[0].text,var[0],var[1])
        else:
            errorMessage("Wrong type in POPS",32)
############################################ READ ##################################################################
    elif instruction.attrib["opcode"].upper() == "READ": #var type
        if STDINInput: #ak je STDIN input true
            inputl = input()
        else:
            inputl = argv_input.readline().split("\n")[0]
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
            errorMessage("Wrong type in READ",53)
######################################### WRITE #################################################
    elif instruction.attrib["opcode"].upper() == "WRITE":  #<symb>
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
        elif instruction[0].attrib["type"] == "nil":
            print("",end='')
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
                print("",end='')
            else:
                errorMessage("Wrong type in WRITE",53)
        else:
            errorMessage("Wrong type in WRITE",53)



    counter += 1
    counter_instruction += 1
