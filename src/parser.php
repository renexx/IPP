<?php
/**
 * Project: IPP project
 *
 * @brief parser.php
 * @author René Bolf         <xbolfr00@stud.fit.vutbr.cz>
 */


$objekt = new Parser;
$objekt->parse();
$objektArgument = new CheckArgumentsAndError;
$objektArgument->parseArguments($argc,$argv);

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
                echo "hovno\n";
                exit(0);
            }
            else
                self::errorMessage("Bad argument",10);
        }

    }
    public static function showHelp()
    {

        echo "hovno\n";
        exit(0);
    }

    public static function errorMessage($message,$exitCode)
    {
        fclose(STDIN);
        $message .= "\n";
        fwrite(STDERR,$message);
        exit($exitCode);
    }
    public static function checkXMLentities()
    {

    }
}
class Parser
{

    public function parse()
    {
        //XML
//**********************************************************************************************
        $xml = new DOMDocument("1.0", "UTF-8"); //vytvori xml s hlavickou 1.0 a UTF-8
        $xml->formatOutput = true; //aby bol format taky aky je pod sebou a nie vedla seba
        $program = $xml->createElement("program"); //vytvori element program
        $program->setAttribute("language","IPPcode19"); //a nastavi mu atribut
        $xml->appendChild($program);//program je decko xml elementu

        $order = 1; //toto je pocitanie order začina od 1

//************* Vytvorenie pola
        if($line = fgets(STDIN))
        {
            $trimline = trim($line);
            if(!preg_match('/^(.IPPcode19)*$/i',$trimline,$matchHeader))
                CheckArgumentsAndError::errorMessage("Missing header .IPPcode19",21);
        }
        else
        {
            CheckArgumentsAndError::errorMessage("ERROR INPUT ",11);
        }

        while($line = fgets(STDIN)) // nacitanie vstupu
        {
            $line = trim(preg_replace("/#.*$/", "", $line)); //zrusenie komentov, medzier
            $line = preg_replace("/&/","&amp;",$line);
            $pattern = array("<",">","\"","'");
            $replace = array("&lt;","&gt;","&quot;","&apos;");
            $line = str_replace($pattern,$replace,$line);
            var_dump($line);
            $splitLineToWord = preg_split('/\s+/', $line); // rozdelenie stringu na slova
            var_dump($splitLineToWord);
            if ($line == "" || $line == "\n") //ked bude koment na riadku tak aby ho nebral k uvahu preskoci cely switch a nacita znovu
                continue;

            $instruction = $xml->createElement("instruction");
            $program->appendChild($instruction);
            //*********************************************************************************************************
            $instruction->setAttribute("order",$order); //nastavenie order
            $order++; //zvysovanie toho countra

            $opcodeName = strtoupper($splitLineToWord[0]);
            //$instruction->setAttribute("opcode",$opcodeName);
            switch($opcodeName)
            {
/******************  0 operand *****************************/
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
                    echo "Ja som split vo vnutri\n";
                    var_dump($splitLineToWord);

                    if(preg_match('/^(LF|GF|TF)@([a-zA-Z]|[_|-|\$|&|%\*])([a-zA-Z]|[0-9]|[_|-|\$|&|%|\*])*$/',$splitLineToWord[1],$match))
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

                    if(preg_match('/^int@([\+-]?[0-9])+$/',$splitLineToWord[1],$match))
                    {
                        $var = "int";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^bool@(true|false)$/',$splitLineToWord[1],$match))
                    {
                        $var = "bool";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^string@([^\ \\\\#]|\\\\[0-9]{3})*$/',$splitLineToWord[1],$match))
                    {
                        $var = "string";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^nil@(nil)$/',$splitLineToWord[1],$match))
                    {
                        $var = "nil";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
                    //$this->addAndCheckSymbol($splitLineToWord[1],$match);
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
                    if(preg_match('/^([a-zA-Z]|[_|-|\$|&|%|\*])([a-zA-Z]|[0-9]|[_|-|\$|&|%|\*])*$/',$splitLineToWord[1],$match))
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
                    if(preg_match('/^(GF|LF|TF)@([a-zA-Z]|[_|-|\$|&|%|\*])([a-zA-Z]|[0-9]|[_|-|\$|&|%|\*])*$/',$splitLineToWord[1],$match))
                    {
                        $this->addVarToXML($xml,$instruction,$match,$i);
                    }
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
                    $i += 1;
/************************* symb ***********************************************/
                    if(preg_match('/^int@([\+-]?[0-9])+$/',$splitLineToWord[2],$match))
                    {
                        $var = "int";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^bool@(true|false)$/',$splitLineToWord[2],$match))
                    {
                        $var = "bool";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^string@([^\ \\\\#]|\\\\[0-9]{3})*$/',$splitLineToWord[2],$match))
                    {
                        $var = "string";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^nil@(nil)$/',$splitLineToWord[2],$match))
                    {
                        $var = "nil";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
                    break;
/****************** 2 operands <var><type>*************************************/
                case "READ":
                    if (count($splitLineToWord) != 3)
                    {
                        CheckArgumentsAndError::errorMessage("Wrong count of operands",23);
                    }
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                    if(preg_match('/^(GF|LF|TF)@([a-zA-Z]|[_|-|\$|&|%|\*])([a-zA-Z]|[0-9]|[_|-|\$|&|%|\*])*$/',$splitLineToWord[1],$match))
                        $this->addVarToXML($xml,$instruction,$match,$i);
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
                    $i += 1;

                    if(preg_match('/^(int|string|bool)$/',$splitLineToWord[2],$match))
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
                    if(preg_match('/^(GF|LF|TF)@([a-zA-Z]|[_|-|\$|&|%|\*])([a-zA-Z]|[0-9]|[_|-|\$|&|%|\*])*$/',$splitLineToWord[1],$match))
                        $this->addVarToXML($xml,$instruction,$match,$i);
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
                    $i += 1;
/************************* symb1 ***********************************************/
                    if(preg_match('/^int@([\+-]?[0-9])+$/',$splitLineToWord[2],$match))
                    {
                        $var = "int";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^bool@(true|false)$/',$splitLineToWord[2],$match))
                    {
                        $var = "bool";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^string@([^\ \\\\#]|\\\\[0-9]{3})*$/',$splitLineToWord[2],$match))
                    {
                        $var = "string";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^nil@(nil)$/',$splitLineToWord[2],$match))
                    {
                        $var = "nil";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
    /************************* symb2 ***********************************************/
                    $i = 3;
                    if(preg_match('/^int@([\+-]?[0-9])+$/',$splitLineToWord[3],$match))
                    {
                        $var = "int";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^bool@(true|false)$/',$splitLineToWord[3],$match))
                    {
                        $var = "bool";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^string@([^\ \\\\#]|\\\\[0-9]{3})*$/',$splitLineToWord[3],$match))
                    {
                        $var = "string";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^nil@(nil)$/',$splitLineToWord[3],$match))
                    {
                        $var = "nil";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }

                    break;
                    //-- 3 operand <label><symb1><symb2>
                case "JUMPIFEQ":
                case "JUMPIFNEQ":
                    if (count($splitLineToWord) != 4)
                    {
                        CheckArgumentsAndError::errorMessage("Wrong count of operands",23);
                    }
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                    if(preg_match('/^([a-zA-Z]|[_|-|\$|&|%|\*])([a-zA-Z]|[0-9]|[_|-|\$|&|%|\*])*$/',$splitLineToWord[1],$match))
                        $this->addLabelToXML($xml,$instruction,$match,$i);
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
                    $i = 2;
                    if(preg_match('/^int@([\+-]?[0-9])+$/',$splitLineToWord[2],$match))
                    {
                        $var = "int";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^bool@(true|false)$/',$splitLineToWord[2],$match))
                    {
                        $var = "bool";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^string@([^\ \\\\#]|\\\\[0-9]{3})*$/',$splitLineToWord[2],$match))
                    {
                        $var = "string";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^nil@(nil)$/',$splitLineToWord[2],$match))
                    {
                        $var = "nil";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }

    /************************* symb2 ***********************************************/
                    $i = 3;
                    if(preg_match('/^int@([\+-]?[0-9])+$/',$splitLineToWord[3],$match))
                    {
                        $var = "int";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^bool@(true|false)$/',$splitLineToWord[3],$match))
                    {
                        $var = "bool";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^string@([^\ \\\\#]|\\\\[0-9]{3})*$/',$splitLineToWord[3],$match))
                    {
                        $var = "string";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }

                    elseif(preg_match('/^nil@(nil)$/',$splitLineToWord[3],$match))
                    {
                        $var = "nil";
                        $this->addSymbToXML($xml,$instruction,$match,$var,$i);
                    }
                    else
                    {
                        CheckArgumentsAndError::errorMessage("Lexical error",23);
                    }
                    break;
                default:
                    CheckArgumentsAndError::errorMessage("Bad operation name",22);
                }

        }
        echo $xml->saveXML();
    }

    public function addAndCheckSymbol($splitLineToWord,$match)
    {
        if(preg_match('/^int@([\+-]?[0-9])+$/',$splitLineToWord[1],$match))
        {
            $this->addSymbToXML($xml,$instruction,$match,$i);
        }

        elseif(preg_match('/^bool@(true|false)$/',$splitLineToWord[1],$match))
        {
            $this->addSymbToXML($xml,$instruction,$match,$i);
        }

        elseif(preg_match('/^string@([^\ \\\\#]|\\\\[0-9]{3})*$/',$splitLineToWord[3],$match))
        {
            $this->addSymbToXML($xml,$instruction,$match,$i);
        }

        elseif(preg_match('/^nil@(nil)$/',$splitLineToWord[1],$match))
        {
            $var = "nil";
            $this->addSymbToXML($xml,$instruction,$match,$i);
        }
        else
        {
            CheckArgumentsAndError::errorMessage("Lexical error",23);
        }
    }
    public function addSymbToXML($xml,$instruction,$match,$var,$i)
    {
        $match = explode("@",$match[0]);
        $argTmp = $xml->createElement("arg$i","$match[1]");
        $argTmp->setAttribute("type",$var);
        $instruction->appendChild($argTmp);
    }
    public function addVarToXML($xml,$instruction,$match,$i)
    {
        $argTmp = $xml->createElement("arg$i","$match[0]");
        $var ="var";
        $argTmp->setAttribute("type",$var);
        $instruction->appendChild($argTmp);
    }
    public function addLabelToXML($xml,$instruction,$match,$i)
    {
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

 ?>
