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
/*$token = new Token;
$token->_construct();*/
/*
class Token
{
    public $tokenType;
    public $tokenAtr;

    public function _construct($tokenType, $tokenAtr)
    {
        $this->token_type = $tokenType;
        $this->token_atr = $tokenAtr;
    }
}
*/
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
        if(!preg_match('/^(.IPPcode19)*$/i',$line))
        {
            echo "MISSIG HEADER"; //dat to na chybovy vystup
            return 21; // navratovy kod pre chybnu hlavicku
        }

        while($line = fgets(STDIN)) // nacitanie vstupu
        {
            $line = trim(preg_replace("/#.*$/", "", $line)); //zrusenie komentov, medzier
            //var_dump($line);
            $splitLineToWord = preg_split('/\s+/', $line); // rozdelenie stringu na slova
            //var_dump($splitLineToWord);
            //$splitLineToWord = explode(" ",$line);// rozdelenie stringu na slova rozdeli to vlastne do pola a slova su indexy
            //$splitLineToWord = preg_split('/\s+/', $line, -1, PREG_SPLIT_NO_EMPTY);
            //if ($line == null || $line == "\n"){
            //cho "toto je slovo rozdelene";
            //var_dump($splitLineToWord);
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
                    $i = 1;
                    $instruction->setAttribute("opcode",$opcodeName);
                    $splitLineToWord = preg_match('/^(GF|LF|TF)@([a-zA-Z]|[\_\-\$\&\%\*])([a-zA-Z]|[0-9]|[\_\-\$\&\%\*])*$/',$splitLineToWord[1],$match);
                    $this->addVarToXML($xml,$instruction,$match,$i);
                    $i += 1;
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

                    break;
                    //-- 3 operand <labe><symb1><symb2>
                case "JUMPIFEQ":
                case "JUMPIFNEQ":

                    break;
                }

        }

        echo $xml->saveXML();
    }
/****************************************************************************/
/*    public function check_label(string $label, array $match) : int
    {
        if(preg_match('/^([a-zA-Z]|[\_\-\$\&\%\*])([a-zA-Z]|[0-9]|[\_\-\$\&\%\*])*$/',$label,$match))
            return 0;
        else
            return 1;
    }*/
/****************************************************************************/
    /*public function check_var($var,$match) : int
    {
        if(preg_match('/^(GF|LF|TF)@([a-zA-Z]|[\_\-\$\&\%\*])([a-zA-Z]|[0-9]|[\_\-\$\&\%\*])*$/',$var,$match))
            return 0;
        else
            return 1;
    }
/****************************************************************************/
    public function check_type($type,$match) : int
    {
        if(preg_match('/^(int|string|bool)$/',$type,$match))
            return 0;
        else
            return 1;
    }
/****************************************************************************/
  public function check_symb($symb,$match) : int
    {
        if(preg_match('/^int@[+-][0-9]+$/',$symb,$match));
/****************************************************************************/
        /*elseif(preg_match('/^bool@(true|false)$/',$symb,$match));
/****************************************************************************/
        /*elseif(preg_match('/^string@([a-zA-Z]|[0-9]|\\\\[0-9]{3}|[\_\-\$\&\%\*])*$/',$symb,$match));
        else return 1;*/
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
}

 ?>
