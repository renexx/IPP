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
                if(argument.attrib["type"] not in ["int","string","bool","nil","var"]):
                    errorMessage("Pri PUSHS, WRITE, EXIT a DPRINT musi byt bud int, string, bool,nil alebo to moze byt var ",32)
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
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "var"):
                    errorMessage("Pri MOVE,INT2CHAR,TYPE,STRLEN musi byt arg1 var",32)
            elif(argument.tag == "arg2"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri MOVE,INT2CHAR,TYPE,STRLEN musi byt arg2 int,string,bool,nil alebo to moze byt var",32)
            else:
                errorMessage("Zle argumenty u MOVE,INT2CHAR,TYPE,STRLEN",32)
            counter_arg += 1
        if(counter_arg != 2):
            errorMessage("Zly pocet argumentov u MOVE,INT2CHAR,TYPE,STRLEN",32)                        
# 2 operandy [var][type] READ
    elif instruction.attrib["opcode"] in ["READ"]:
        counter_arg = 0
        for argument in instruction:
            if "type" not in argument.attrib:
                errorMessage("Chyba type u READ",32)
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "var"):
                    errorMessage("Pri READ musi byt arg1 var",32)
            elif(argument.tag == "arg2"):
                if(argument.attrib["type"] != "type"):
                    errorMessage("Pri READ musi byt arg2 type",32)
            else:
                errorMessage("Zle argumenty u READ",32)
            counter_arg +=1
        if(counter_arg != 2):
            errorMessage("Zly pocet argumentov u READ",32)
#3 operandy [var] [symb1] [symb2] symbol moze byt var, int, string, bool, nil ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR
    elif instruction.attrib["opcode"] in ["ADD","SUB","MUL","IDIV","LT","GT","EQ","AND","OR","NOT","STRI2INT","CONCAT","GETCHAR","SETCHAR"]:
        counter_arg = 0
        for argument in instruction:
            if "type" not in argument.attrib:
                errorMessage("Chyba type u ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR ",32)
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "var"):
                    errorMessage("Pri ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR musi byt arg1 var",32)
            elif(argument.tag == "arg2"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR musi byt arg2 int,string,bool,nil,var",32)
            elif(argument.tag == "arg3"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR musi byt arg3 int,string,bool,nil,var",32)                                                
            else:
                errorMessage("Zle argumenty u ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR",32)
            counter_arg += 1
        if(counter_arg != 3):
            errorMessage("Zly pocet argumentov u ADD,SUB,MUL,IDIV,LT,GT,EQ,AND,OR,NOT,STRI2INT,CONCAT,GETCHAR,SETCHAR",32) 
                  
#3 oprandy [label] [symb1] [symb2]   JUMPIFEQ JUMPIFNEQ              
    elif instruction.attrib["opcode"] in ["JUMPIFEQ","JUMPIFNEQ"]:
        counter_arg = 0
        for argument in instruction:
            if "type" not in argument.attrib:
                errorMessage("Chyba type u JUMPIFEQ, JUMPIFNEQ ",32)
            if(argument.tag == "arg1"):
                if(argument.attrib["type"] != "label"):
                    errorMessage("Pri JUMPIFEQ a JUMPIFNEQ musi byt arg1 label",32)
            elif(argument.tag == "arg2"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri JUMPIFEQ a JUMPIFNEQ musi byt arg2 int,string,bool,nil,var",32)
            elif(argument.tag == "arg3"):
                if argument.attrib["type"] not in ["int","string","bool","nil","var"]:
                    errorMessage("Pri JUMPIFEQ a JUMPIFNEQ musi byt arg3 int,string,bool,nil,var",32)                                                
            else:
                errorMessage("Zle argumenty u JUMPIFEQ a JUMPIFNEQ",32)
            counter_arg += 1
        if(counter_arg != 3):
            errorMessage("Zly pocet argumentov u JUMPIFEQ a JUMPIFNEQ",32) 
    else:
        errorMessage("Neznamy operacny kod",32)


#TODO  zoradit elementy xmlka [DONE]
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
###########################################################################   
                
    counter_order += 1
    reg_variable = "^(LF|GF|TF)@([a-zA-Z]|[_|\-|\$|&|%|\?|\!|\*])([a-zA-Z]|[0-9]|[_|\-|\$|&|%|\?|\!|\*])*$"
    reg_symb_int = "^((\+|-)?[0-9]\d*)$"
    reg_symb_string = "([^\ \\\\#]|\\\\[0-9]{3})*$"
    reg_symb_bool = "^(true|false)$/"
    reg_symb_nil = '^nil@nil$/'; /** regular expression for symbol nil */
    reg_label = "^([a-zA-Z]|[_|\-|\$|&|%|\?|\!|\*])([a-zA-Z]|[0-9]|[_|\-|\$|&|%|\?|\!|\*])*$"
    reg_type = "^(int|string|bool)$"
    
    for instruction in root_program:
        if instruction.attrib["opcode"] 
    #GF = {}
    #TF = None
    #LF = []
    #for instruction in root_program:
    #    variable = instruction[0].text
#        variable_splited = variable.split("@",1)
#        frame = variable_splited[0]
        #if(frame == "GF"):
            #        variable_value = variable_splited[1]
            #G#F[variable_value] = [instruction[0].attrib["type"],instruction[0].text]
        #    print(GF)
    #    else:
    #        errorMessage("nejaky semanticky erro premena aj cislo",32)
    #    if(frame == "TF"):
    #        if(TF == None):
    #            errorMessage("neni dksmds",32)
    #        else:    
    #            TF[variable_value] = [instruction[0].attrib["type"],instruction[0].text]
    #    if(frame == "LF"):
    #        if(LF):
    #            LF[(-1)variable_value] = [instruction[0].attrib["type"],instruction[0].text]
    #        else:
    #            errorMessage("aaasaa",32)                    

# 
                
#LF je prblem cely zasobnik ramcu
#urobime si zasobnik Listom
#LF = []


#if(ramec == "LF"):
#    if LF:
#        LF[(-1)nazov_value] = [instrukce[1].attrib["type"].instrukcie[1].text]
#    else:
#        print chyba    
#je to list a ked pride pushframe tak do toho listu 
#LF.append({}) pridame do neho slovnik
#if LF:
#    LF.pop() ak nepojde pushframe ak tam insensitive mozne sa stat ze tam bude popframe
                
#ak pride CREATEFRAME
#TF= {}
               
#dom.write("example.xml")

