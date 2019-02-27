<?php
/**
 * Project: IPP project
 *
 * @brief parser.php
 * @author René Bolf         <xbolfr00@stud.fit.vutbr.cz>
 */


public static function showHelp()
{
    echo("este neviem co sem napisem to az potom nakoniec spravim");

}    */
$objekt = new Parser;
$objekt->parse();
$token = new Token;
$token->_construct();

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
class Parser
{
    public function parse()
    {
        //XML
//**********************************************************************************************
        $xml = new DOMDocument("1.0", "UTF-8");
        $xml->formatOutput = true; //aby bol format taky aky je pod sebou a nie vedla seba
        $program = $xml->createElement("program");
        $program->setAttribute("language","IPPcode19");
        $xml->appendChild($program);

        $order = 1; //toto je pocitanie order začina od 1

//************* Vytvorenie pola

        while($line = fgets(STDIN)); // nacitanie vstupu
        {

            $line = preg_replace("~#.*~", "", $line); //zrusenie komentov, medzier
            $splitLineToWord = preg_split('/\s+/', $line); // rozdelenie stringu na slova
            //if ($line == null || $line == "\n"){
            $instruction = $xml->createElement("instruction");
            $program->appendChild($instruction);
            //*********************************************************************************************************
            $instruction->setAttribute("order",$order); //nastavenie order
            $order++; //zvysovanie toho countra

            if(!preg_match('/^(.IPPcode19)*$/i'))
            }
                fprint(STDERR, "Missing header");// hlavicka //  /i znamena ze je to case insensitive
                return 21; // navratovy kod pre chybnu hlavicku
            {


                $opcodeName[0] = strtoupper($splitLineToWord[0]);
                $instruction->setAttribute("opcode",strtoupper($opcodeName));
                switch($opcodeName[0] = strtoupper($splitLineToWord[0]))
                {
/******************  0 operand *****************************/
                    case "CREATEFRAME":
                    case "PUSHFRAME":
                    case "POPFRAME":
                    case "RETURN":
                    case "BREAK":
                        if (count($splitLineToWord) != 1)
                            return 23;

                        break;
/****************** 1 operand <var>********************************************/
                    case "DEFVAR":
                    case "POPS":
                        if (count($splitLineToWord) != 2)
                            return 23;
                        check_var();
                        break;
/****************** 1 operand <symb>*******************************************/
                    case "PUSH":
                    case "WRITE":
                    case "EXIT":
                    case "DPRINT":
                        if (count($splitLineToWord) != 2)
                            return 23;
                        check_symb;
                        break;
/****************** 1 operand <label>******************************************/
                    case "CALL":
                    case "LABEL":
                    case "JUMP":
                        if (count($splitLineToWord) != 2)
                            return 23;
                        check_label();
                        break;
/****************** 2 operands <var><symb>*************************************/
                    case "MOVE":
                    case "INT2CHAR":
                    case "TYPE":
                    case "STRLEN":
                        if (count($splitLineToWord) != 3)
                            return 23;
                        check_var();
                        check_symb();
                        break;
/****************** 2 operands <var><type>*************************************/
                    case "READ":
                        if (count($splitLineToWord) != 3)
                            return 23;
                        check_var();
                        check_type();
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
                            return 23;
                            check_var();
                            check_symb();
                            check_symb();
                        break;
                    //-- 3 operand <labe><symb1><symb2>
                    case "JUMPIFEQ":
                    case "JUMPIFNEQ":
                        if (count($splitLineToWord) != 4)
                            return 23;
                            check_label();
                            check_symb();
                            check_symb();
                        break;
                }

        }

        echo $xml->saveXML();
    }
    public function check_label()
    {
        if(preg_match('/^(GF|LF|TF)@([a-zA-Z]|[\_\-\$\&\%\*])([a-zA-Z]|[0-9]|[\_\-\$\&\%\*])*$/')
    }
    public function check_var()
    {
        if(preg_match('/^(GF|LF|TF)@([a-zA-Z]|[\_\-\$\&\%\*])([a-zA-Z]|[0-9]|[\_\-\$\&\%\*])*$/')
    }
    public function check_type()
    {
        if(preg_match('/^(int|string|bool)$/')
    }
    public function check_symb()
    {
        if(preg_match('/^int@[+-][0-9]+$/')
        if(preg_match('/^bool@(true|false)$/')
        if(preg_match('/^string@([a-zA-Z]|[0-9]|\\\\[0-9]{3}|[\_\-\$\&\%\*])*$/'/)
    }
}

 ?>
