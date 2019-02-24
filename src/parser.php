<?php
/**
 * Project: IPP project
 *
 * @brief parser.php
 * @author René Bolf         <xbolfr00@stud.fit.vutbr.cz>
 */

/*class Token
{
    public $tokenType;
    public $tokenAtr;

    function _construct($tokenType,$tokenAtr)
    {
        $this->$tokenType = $tokenType;
        $this->$tokenAtr = $tokenAtr;

    }
}
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

        $order_counter = 1; //toto je pocitanie order začina od 1

//************* Vytvorenie pola
       $opcodeName = array("MOVE"=>"MOVE", //    <var><symb>
       "CREATEFRAME"=>"CREATEFRAME",
       "PUSHFRAME"=>"PUSHFRAME",
       "POPFRAME"=>"POPFRAME",
       "DEFVAR"=>"DEFVAR",//<var>
       "CALL"=>"CALL", //<label>
       "RETURN"=>"RETURN",
       "PUSHS"=>"PUSHS",//<symb>
       "POPS"=>"POPS",//<var>
       "ADD"=>"ADD",//<var><symb1><symb2>
       "SUB"=>"SUB",//<var><symb1><symb2>
       "MUL"=>"MUL",//<var><symb1><symb2>
       "IDIV"=>"IDIV",//<var><symb1><symb2>
       "LT"=>"LT",//<var><symb1><symb2>
       "GT"=>"GT",//<var><symb1><symb2>
       "EQ"=>"EQ",//<var><symb1><symb2>
       "AND"=>"AND",//<var><symb1><symb2>
       "OR"=>"OR",//<var><symb1><symb2>
       "NOT"=>"NOT",//<var><symb1><symb2>
       "INT2CHAR"=>"INT2CHAR", //<var><symb>
       "STRI2INT"=>"STRI2INT",//<var><symb1><symb2>
       "READ"=>"READ",//<var><type>
       "WRITE"=>"WRITE",//<symb>
       "CONCAT"=>"CONCAT",//<var><symb1><symb2>
       "STRLEN"=>"STRLEN",//var><symb>
       "GETCHAR"=>"GETCHAR",//<var><symb1><symb2>
       "SETCHAR"=>"SETCHAR",//<var><symb1><symb2>
       "TYPE"=>"TYPE",//var><symb>
       "LABEL"=>"LABEL",//<label>
       "JUMP"=>"JUMP",//<label>
       "JUMPIFEQ"=>"JUMPIFEQ", //<var><symb1><symb2>
       "JUMPIFNEQ"=>"JUMPIFNEQ",//<var><symb1><symb2>
        "EXIT"=>"EXIT", //<symb>
        "DPRINT"=>"DPRINT", //<symb>
        "BREAK"=>"BREAK");
        while($line = fgets(STDIN)); // nacitanie vstupu ale iba jedneho riadku
        {
            //if ($line == null || $line == "\n"){
            $instruction = $xml->createElement("instruction");
            $program->appendChild($instruction);


            //*********************************************************************************************************
            $instruction->setAttribute("order",$order_counter); //nastavenie order
            $order_counter++; //zvysovanie toho countra
            $instruction->setAttribute("opcode",strtoupper($opcodeName));       /* TODO*/
            for($i = 1; $i < func_num_args(); $i++)
            {
                $argToken = func_get_arg($i);
                switch($argToken->$tokenType)
                {
                    case "var":
                        $argElement = $xml->createElement("arg".$i,$argToken->$tokenAtr);
                        $argElement->setAttribute("type","var");
                        break;
                    case 'label':
                        $argElement = $xml->createElement("arg".$i,$argToken->$tokenAtr);
                        $argElement->setAttribute("type","label");
                        break;
                    case 'type':
                        $argElement = $xml->createElement("arg".$i,$argToken->$tokenAtr);
                        $argElement->setAttribute("type","type");
                        break;
                    case 'int':
                        $argElement = $xml->createElement("arg".$i,$argToken->$tokenAtr);
                        $argElement->setAttribute("type","int");
                        break;
                    case 'bool':
                        $argElement = $xml->createElement("arg".$i,$argToken->$tokenAtr);
                        $argElement->setAttribute("type","bool");
                        break;
                    case 'string':
                        $argElement = $xml->createElement("arg".$i,$argToken->$tokenAtr);
                        $argElement->setAttribute("type","string");
                        break;
                    default:
                            echo "error";
                }
            $instruction->appendChild($argElement);
            }
            ///}
        }

        echo $xml->saveXML();
    }
}
(preg_match('/^(GF|LF|TF)@([a-zA-Z]|[\_\-\$\&\%\*])([a-zA-Z]|[0-9]|[\_\-\$\&\%\*])*$/'//var
preg_match('/^int@[+-][0-9]+$/'//int
preg_match('/^bool@(true|false)$/'//bool
preg_match('/^string@([a-zA-Z]|[0-9]|\\\\[0-9]{3}|[\_\-\$\&\%\*])*$/'//string
preg_match('/^(int|string|bool)$/', //type
preg_match('/^([a-zA-Z]|[\_\-\$\&\%\*])([a-zA-Z]|[0-9]|[\_\-\$\&\%\*])*$/' //label




 ?>
