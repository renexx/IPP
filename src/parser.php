<?php 
/**
 * Project: IPP project
 *
 * @brief parser.php
 * @author René Bolf         <xbolfr00@stud.fit.vutbr.cz>
 */

class Token
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
    
}    







 ?>