<?php
/**
 * Project: IPP project
 *
 * @brief parser.php
 * @author René Bolf         <xbolfr00@stud.fit.vutbr.cz>
 */


/*public static function showHelp()
{
    echo("este neviem co sem napisem to az potom nakoniec spravim");

}    */
$objekt = new Parser;
$objekt->parse();

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
        $line = fgets(STDIN);
        $headerIPP = preg_match('/^(.IPPcode19)*$/i',$line);
        $trimedheaderIPP = trim($headerIPP);
        if ($trimedheaderIPP != $headerIPP)
        {
            echo "Missing header .IPPcode19"; //dat to na chybovy vystup
            return 21; // navratovy kod pre chybnu hlavicku
        }

        while($line = fgets(STDIN)) // nacitanie vstupu
        {
            $line = trim(preg_replace("/#.*$/", "", $line)); //zrusenie komentov, medzier
            $splitLineToWord = preg_split('/\s+/', $line); // rozdelenie stringu na slova

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
                    //if (count($splitLineToWord) != 1)
                      // return 23;

                    $instruction->setAttribute("opcode",$opcodeName);
                    break;
/****************** 1 operand <var>********************************************/
                case "DEFVAR":
                case "POPS":
                        $i = 1;
                        $instruction->setAttribute("opcode",$opcodeName);
                        $splitLineToWord = preg_match('/^(GF|LF|TF)@([a-zA-Z]|[\_\-\$\&\%\*])([a-zA-Z]|[0-9]|[\_\-\$\&\%\*])*$/',$splitLineToWord[1],$match);
                        $this->addVarToXML($xml,$instruction,$match,$i);

                    //}
                    break;
/****************** 1 operand <symb>*******************************************/
                case "PUSH":
                case "WRITE":
                case "EXIT":
                case "DPRINT":
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                    if(preg_match('/^int@[+-][0-9]+$/',$splitLineToWord[1],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }

                    if(preg_match('/^bool@(true|false)$/',$splitLineToWord[1],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }

                    if(preg_match('/^string@([a-zA-Z]|[0-9]|\\\\[0-9]{3}|[\_\-\$\&\%\*])*$/',$splitLineToWord[1],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }


                    break;
/****************** 1 operand <label>******************************************/
                case "CALL":
                case "LABEL":
                case "JUMP":
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                    $splitLineToWord = preg_match('/^([a-zA-Z]|[\_\-\$\&\%\*])([a-zA-Z]|[0-9]|[\_\-\$\&\%\*])*$/',$splitLineToWord[1],$match);
                    $this->addLabelToXML($xml,$instruction,$match,$i);
                    break;
/****************** 2 operands <var><symb>*************************************/
                case "MOVE":
                case "INT2CHAR":
                case "TYPE":
                case "STRLEN":
/************************** var ************************************************/
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                    if(preg_match('/^(GF|LF|TF)@([a-zA-Z]|[\_\-\$\&\%\*])([a-zA-Z]|[0-9]|[\_\-\$\&\%\*])*$/',$splitLineToWord[1],$match))
                        $this->addVarToXML($xml,$instruction,$match,$i);
                    $i += 1;
/************************* symb ***********************************************/
                    if(preg_match('/^int@[+-][0-9]+$/',$splitLineToWord[2],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }

                    if(preg_match('/^bool@(true|false)$/',$splitLineToWord[2],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }

                    if(preg_match('/^string@([a-zA-Z]|[0-9]|\\\\[0-9]{3}|[\_\-\$\&\%\*])*$/',$splitLineToWord[2],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }
                    break;
/****************** 2 operands <var><type>*************************************/
                case "READ":
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                    if(preg_match('/^(GF|LF|TF)@([a-zA-Z]|[\_\-\$\&\%\*])([a-zA-Z]|[0-9]|[\_\-\$\&\%\*])*$/',$splitLineToWord[1],$match))
                        $this->addVarToXML($xml,$instruction,$match,$i);
                    $i += 1;

                    if(preg_match('/^(int|string|bool)$/',$splitLineToWord[2],$match))
                        $this->addTypeToXML($xml,$instruction,$match,$i);
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
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                    if(preg_match('/^(GF|LF|TF)@([a-zA-Z]|[\_\-\$\&\%\*])([a-zA-Z]|[0-9]|[\_\-\$\&\%\*])*$/',$splitLineToWord[1],$match))
                        $this->addVarToXML($xml,$instruction,$match,$i);
                    $i += 1;
/************************* symb1 ***********************************************/
                    if(preg_match('/^int@[+-][0-9]+$/',$splitLineToWord[2],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }

                    if(preg_match('/^bool@(true|false)$/',$splitLineToWord[2],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }

                    if(preg_match('/^string@([a-zA-Z]|[0-9]|\\\\[0-9]{3}|[\_\-\$\&\%\*])*$/',$splitLineToWord[2],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }
    /************************* symb2 ***********************************************/
                    $i = 3;
                    if(preg_match('/^int@[+-][0-9]+$/',$splitLineToWord[3],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }

                    if(preg_match('/^bool@(true|false)$/',$splitLineToWord[3],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }

                    if(preg_match('/^string@([a-zA-Z]|[0-9]|\\\\[0-9]{3}|[\_\-\$\&\%\*])*$/',$splitLineToWord[3],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }
                    break;
                    //-- 3 operand <labe><symb1><symb2>
                case "JUMPIFEQ":
                case "JUMPIFNEQ":
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                    if(preg_match('/^([a-zA-Z]|[\_\-\$\&\%\*])([a-zA-Z]|[0-9]|[\_\-\$\&\%\*])*$/',$splitLineToWord[1],$match))
                        $this->addLabelToXML($xml,$instruction,$match,$i);

                    $i = 2;
                    if(preg_match('/^int@[+-][0-9]+$/',$splitLineToWord[2],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }

                    if(preg_match('/^bool@(true|false)$/',$splitLineToWord[2],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }

                    if(preg_match('/^string@([a-zA-Z]|[0-9]|\\\\[0-9]{3}|[\_\-\$\&\%\*])*$/',$splitLineToWord[2],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }
    /************************* symb2 ***********************************************/
                    $i = 3;
                    if(preg_match('/^int@[+-][0-9]+$/',$splitLineToWord[3],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }

                    if(preg_match('/^bool@(true|false)$/',$splitLineToWord[3],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }

                    if(preg_match('/^string@([a-zA-Z]|[0-9]|\\\\[0-9]{3}|[\_\-\$\&\%\*])*$/',$splitLineToWord[3],$match))
                    {
                        $this->addSymbToXML($xml,$instruction,$match,$i);
                    }
                    break;
                default:
                        echo "zly operacny kod";
                        return 22;
                }

        }
        echo $xml->saveXML();
    }

    public function addSymbToXML($xml,$instruction,$match,$i)
    {
        $argTmp = $xml->createElement("arg$i","$match[0]");
        $var ="symb";
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
