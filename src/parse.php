<?php
/**
 * Project: IPP project
 *
 * @brief parse.php
 * @author René Bolf         <xbolfr00@stud.fit.vutbr.cz>
 */

class CheckArgumentsAndError
{
    public function parseArguments($argc,$argv)
    {
        if($argc > 2)
        {
            self::errorMessage("Wrong count of arguments",10);
        }
        elseif ($argc === 2)
        {

            if($argv[1] === "--help")
            {
                self::showHelp();
            }
            else
                self::errorMessage("Bad argument",10);
        }
    }
    public static function showHelp()
    {
        echo "\n**********************************HELP**************************************************************************\n";
        echo "RUN : php7.3 parse.php [--help]\n";
        echo "HELP : --help\t print help\n";
        echo "parse.php is a script type of filter. This script load source code IPPcode19(see section 6)\nfrom standrart input and check lexical and syntax correctness of code\n";
        echo "script parse.php generate XML representation of code to the standart output according to the specification(see section 3.1)\n";
        echo "\n******************************ERROR CODE*************************************************************************\n";
        echo "21 - wrong or missing header in the source code written in IPPcode19. Right header is .IPPcode19 (case insensitive)\n";
        echo "22 - unknown or wrong operation code(case insensitive) in the source code written in IPPcode19\n";
        echo "23 - other lexical or syntax error of the source code wrote in IPPcode19\n ";
        echo "\n******************************IPPcode19**************************************************************************\n";
        echo "Unstructured imperative language includes three-line instuctions.\n";
        echo "Each instruction consist of the operating code (case insensitive) and operands (case sensitive)\n";
        echo "There is a maximum of one instruction per line and it is not allowed to write one instruction on multiple rows\n";
        echo "Each operand is a variable,constant,type or label.\n";
        echo "Comment - # is a one-line comment\n";
        echo "Code starts with header (.IPPcode19)\n";
        exit(0);
    }

    public static function errorMessage($message,$exitCode)
    {
        fclose(STDIN);
        $message .= "\n";
        fwrite(STDERR,$message);
        exit($exitCode);
    }
}

class Parser
{
    public $variable = '/^(LF|GF|TF)@([a-zA-Z]|[_|-|\$|&|%|\?|\!|\*])([a-zA-Z]|[0-9]|[_|-|\$|&|%|\?|\!|\*])*$/';
    public $symbInt = '/^int@([\+-]?[0-9])+$/';
    public $symbString = '/^string@([^\ \\\\#]|\\\\[0-9]{3})*$/';
    public $symbBool = '/^bool@(true|false)$/';
    public $symbNil = '/^nil@nil$/';
    public $label = '/^([a-zA-Z]|[_|-|\$|&|%|\?|\!|\*])([a-zA-Z]|[0-9]|[_|-|\$|&|%|\?|\!|\*])*$/';
    public $type = '/^(int|string|bool)$/';
    
    public function parse()
    {
        $xml = new DOMDocument("1.0", "UTF-8"); /*create xml with header 1.0 a UTF-8*/
        $xml->formatOutput = true; /*for better format*/
        $program = $xml->createElement("program"); /*create element program*/
        $program->setAttribute("language","IPPcode19"); /*set attribut program*/
        $xml->appendChild($program);/*program is a child xml element*/

        $order = 1; /*order counter*/

        $line = fgets(STDIN);
        $trimline = trim(preg_replace("/#.*$/", "",$line)); /*Strip whitespace (or other characters) from the beginning and end of a string*/
        if(!preg_match('/^.IPPcode19$/i',$trimline,$matchHeader))
            CheckArgumentsAndError::errorMessage("Missing header .IPPcode19",21);

        while($line = fgets(STDIN)) /*load input*/
        {
            $line = trim(preg_replace("/#.*$/", "", $line)); /*delete comments and whitespace*/
            $splitLineToWord = preg_split('/\s+/', $line); /*split string to  words*/

            if ($line == "" || $line == "\n") /*when comment or enter is on on the line skip switch*/
                continue;

            $instruction = $xml->createElement("instruction");
            $program->appendChild($instruction);
            $instruction->setAttribute("order",$order);
            $order++;

            $opcodeName = strtoupper($splitLineToWord[0]);

            switch($opcodeName)
            {
/******************  0 operand *************************************************/
                case "CREATEFRAME":
                case "PUSHFRAME":
                case "POPFRAME":
                case "RETURN":
                case "BREAK":
                    if (count($splitLineToWord) != 1)
                    {
                        CheckArgumentsAndError::errorMessage("Wrong count of operands",23);
                    }
                    $instruction->setAttribute("opcode",$opcodeName);
                    break;
/****************** 1 operand <var>********************************************/
                case "DEFVAR":
                case "POPS":
                    if (count($splitLineToWord) != 2)
                    {
                        CheckArgumentsAndError::errorMessage("Wrong count of operands",23);
                    }
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);

                    if(preg_match($this->variable,$splitLineToWord[1],$match))
                    {
                        $this->addVarToXML($xml,$instruction,$match,$i);
                    }
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
                    break;
/****************** 1 operand <symb>*******************************************/
                case "PUSH":
                case "WRITE":
                case "EXIT":
                case "DPRINT":
                    if (count($splitLineToWord) != 2)
                    {
                        CheckArgumentsAndError::errorMessage("Wrong count of operands",23);
                    }
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                        
                    $this->checkSymbol($splitLineToWord,1,$xml,$instruction,$i); /*1 is a position*/
                    
                    break;
/****************** 1 operand <label>******************************************/
                case "CALL":
                case "LABEL":
                case "JUMP":
                    if (count($splitLineToWord) != 2)
                    {
                        CheckArgumentsAndError::errorMessage("Wrong count of operands",23);
                    }
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                    if(preg_match($this->label,$splitLineToWord[1],$match))
                    {
                        $this->addLabelToXML($xml,$instruction,$match,$i);
                    }
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }

                    break;
/****************** 2 operands <var><symb>*************************************/
                case "MOVE":
                case "INT2CHAR":
                case "TYPE":
                case "STRLEN":
                    if (count($splitLineToWord) != 3)
                    {
                        CheckArgumentsAndError::errorMessage("Wrong count of operands",23);
                    }
/************************** var ************************************************/
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                    if(preg_match($this->variable,$splitLineToWord[1],$match))
                    {
                        $this->addVarToXML($xml,$instruction,$match,$i);
                    }
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
                    $i += 1;
/************************* symb ***********************************************/
                    $this->checkSymbol($splitLineToWord,2,$xml,$instruction,$i); /* 2 is a position */
                    break;
/****************** 2 operands <var><type>*************************************/
                case "READ":
                    if (count($splitLineToWord) != 3)
                    {
                        CheckArgumentsAndError::errorMessage("Wrong count of operands",23);
                    }
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                    if(preg_match($this->variable,$splitLineToWord[1],$match))
                        $this->addVarToXML($xml,$instruction,$match,$i);
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
                    $i += 1;

                    if(preg_match($this->type,$splitLineToWord[2],$match))
                        $this->addTypeToXML($xml,$instruction,$match,$i);
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
                    break;
/****************** 3 operands <var><symb1><symb2>*****************************/
                case "ADD":
                case "SUB":
                case "MUL":
                case "IDIV":
                case "LT":
                case "GT":
                case "EQ":
                case "AND":
                case "OR":
                case "NOT":
                case "STRI2INT":
                case "CONCAT":
                case "GETCHAR":
                case "SETCHAR":
                    if (count($splitLineToWord) != 4)
                    {
                        CheckArgumentsAndError::errorMessage("Wrong count of operands",23);
                    }
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                    if(preg_match($this->variable,$splitLineToWord[1],$match))
                        $this->addVarToXML($xml,$instruction,$match,$i);
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
                    $i += 1;
/************************* symb1 ***********************************************/
                    $this->checkSymbol($splitLineToWord,2,$xml,$instruction,$i); /* 2 is a position */
/************************* symb2 ***********************************************/
                    $i = 3;
                    $this->checkSymbol($splitLineToWord,3,$xml,$instruction,$i); /* 3 is a position */

                    break;
/************************** 3 operand <label><symb1><symb2>********************/
                case "JUMPIFEQ":
                case "JUMPIFNEQ":
                    if (count($splitLineToWord) != 4)
                    {
                        CheckArgumentsAndError::errorMessage("Wrong count of operands",23);
                    }
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
/******************************** <label>***************************************/                    
                    if(preg_match($this->label,$splitLineToWord[1],$match))
                        $this->addLabelToXML($xml,$instruction,$match,$i);
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
/******************************** <symb1> **************************************/                    
                    $i = 2;
                    $this->checkSymbol($splitLineToWord,2,$xml,$instruction,$i);

/******************************** <symb2> **************************************/
                    $i = 3;
                    $this->checkSymbol($splitLineToWord,3,$xml,$instruction,$i);
                    break;
                default:
                    CheckArgumentsAndError::errorMessage("Bad operation name",22);
                }

        }
        echo $xml->saveXML();
    }
    public function checkSymbol($splitLineToWord,$position,$xml,$instruction,$i)
    {
        if(preg_match($this->variable,$splitLineToWord[$position],$match))
        {
            $var = "var";
            $this->addVarToXML($xml,$instruction,$match,$i);
        }
        elseif(preg_match($this->symbInt,$splitLineToWord[$position],$match))
        {
            $var = "int";
            $this->addSymbToXML($xml,$instruction,$match,$var,$i);
        }

        elseif(preg_match($this->symbBool,$splitLineToWord[$position],$match))
        {
            $var = "bool";
            $this->addSymbToXML($xml,$instruction,$match,$var,$i);
        }

        elseif(preg_match($this->symbString,$splitLineToWord[$position],$match))
        {
            $var = "string";
            $this->addSymbToXML($xml,$instruction,$match,$var,$i);
        }

        elseif(preg_match($this->symbNil,$splitLineToWord[$position],$match))
        {
            $var = "nil";
            $this->addSymbToXML($xml,$instruction,$match,$var,$i);
        }
        else
        {
            CheckArgumentsAndError::errorMessage("Lexical error",23);
        }
    }

    public function addSymbToXML($xml,$instruction,$match,$var,$i)
    {
        $match = preg_replace("/&/","&amp;",$match);
        $pattern = array("<",">","\"","'");
        $replace = array("&lt;","&gt;","&quot;","&apos;");
        $match = str_replace($pattern,$replace,$match);

        $match = explode("@",$match[0]);
        $argTmp = $xml->createElement("arg$i","$match[1]");
        $argTmp->setAttribute("type",$var);
        $instruction->appendChild($argTmp);
    }
    public function addVarToXML($xml,$instruction,$match,$i)
    {
        $match = preg_replace("/&/","&amp;",$match);

        $argTmp = $xml->createElement("arg$i","$match[0]");
        $var ="var";
        $argTmp->setAttribute("type",$var);
        $instruction->appendChild($argTmp);
    }
    public function addLabelToXML($xml,$instruction,$match,$i)
    {
        $match = preg_replace("/&/","&amp;",$match);

        $argTmp = $xml->createElement("arg$i","$match[0]");
        $var ="label";
        $argTmp->setAttribute("type",$var);
        $instruction->appendChild($argTmp);
    }
    public function addTypeToXML($xml,$instruction,$match,$i)
    {
        $argTmp = $xml->createElement("arg$i","$match[0]");
        $var ="type";
        $argTmp->setAttribute("type",$var);
        $instruction->appendChild($argTmp);
    }
}
/*************** MAIN *******************************************************/
$objektArgument = new CheckArgumentsAndError;
$objektArgument->parseArguments($argc,$argv);
$objekt = new Parser;
$objekt->parse();
 ?>
