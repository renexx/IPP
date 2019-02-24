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
        $instruction = $xml->createElement("instruction");
        $program->appendChild($instruction);


//*********************************************************************************************************
       $order_counter = 1; //toto je pocitanie order začina od 1
       $instruction->setAttribute("order",$order_counter); //nastavenie order
       $order_counter++; //zvysovanie toho countra
       $instruction->setAttribute("opcode",strtoupper($opcodeName));
//************* Vytvorenie pola
       $opcodeName = array("MOVE", //    <var><symb>
       "CREATEFRAME",
       "PUSHFRAME",
       "POPFRAME",
       "DEFVAR",//<var>
       "CALL", //<label>
       "RETURN",
       "PUSHS",//<symb>
       "POPS",//<var>
       "ADD",//<var><symb1><symb2>
       "SUB",//<var><symb1><symb2>
       "MUL",//<var><symb1><symb2>
       "IDIV",//<var><symb1><symb2>
       "LT",//<var><symb1><symb2>
       "GT",//<var><symb1><symb2>
       "EQ",//<var><symb1><symb2>
       "AND",//<var><symb1><symb2>
       "OR",//<var><symb1><symb2>
       "NOT",//<var><symb1><symb2>
       "INT2CHAR", //<var><symb>
       "STRI2INT",//<var><symb1><symb2>
       "READ",//<var><type>
       "WRITE",//<symb>
       "CONCAT",//<var><symb1><symb2>
       "STRLEN",//var><symb>
       "GETCHAR",//<var><symb1><symb2>
       "SETCHAR",//<var><symb1><symb2>
       "TYPE",//var><symb>
       "LABEL",//<label>
       "JUMP",//<label>
       "JUMPIFEQ", //<var><symb1><symb2>
       "JUMPIFNEQ",//<var><symb1><symb2>
        "EXIT", //<symb>
        "DPRINT", //<symb>
        "BREAK")
       echo $xml->saveXML();
        while($line = fgets(STDIN)); // nacitanie vstupu ale iba jedneho riadku
        {
            //if ($line == null || $line == "\n"){
                ;
            ///}
        }
    }
}







 ?>
