<?php
/*
kazdy test je tvoreny az 4 subormi src,in,out a rc
src - obsahuje zdrojovy kod v jazyku IPPcode19
in,out,rc - obsahuju vstup a ocakavany referencny vystupo interpetacie a očakavany prvy chybovy navratovy kod analyzy a interpetacie alebo bezchybovy
vystup 0
ak subor s priponou in alebo out chyba tak sa automaticky dogeneruje prazdny subor
ak chyba rc tak sa vygeneruje subor obsahujuci navratovu hodnotu 0*/

class CheckArgumentsAndError
{

    public $recursive;
    public $directory;
    public $parser;
    public $interpret;
    public $parseonly;
    public $intonly;

    public function __construct()
    {
        $this->recursive = false;
        $this->parser = realpath("./parse.php");
        $this->interpret = realpath("./interpret.py");
        $this->parseonly = false;
        $this->intonly = false;
        $this->directory = realpath("./");
        if(!is_dir($this->directory))
        {
            self::errorMessage("Specified directory is not a directory",11);
        }
        $this->directory = $this->directory."/";
    }

    public function parseArguments($argv,$argc)
    {

        $options = array("help","directory::","recursive","parse-script::","int-script::","parse-only","int-only");
        $opts = getopt("",$options);
        if(count($opts) != $argc - 1)
        {
            self::errorMessage("Bad arguments",10);
        }
        if($argc === 2)
        {
            if(isset($opts["help"]))
            {
                if($argv[1] === "--help")
                {
                    self::showHelp();
                }
            }
            if(isset($opts["directory"]))
            {
                if(!is_dir($opts["directory"]))
                {
                    self::errorMessage("Specified directory is not a directory",11);
                }
                $this->directory = realpath($opts["directory"])."/";
                print("riadok 57");
                var_dump($this->directory);

            }
            if(isset($opts["recursive"]))
            {
                $this->recursive = true;
            }
            if(isset($opts["parse-script"]))
            {
                $this->parser = $opts["parse-script"];
            }
            if(isset($opts["int-script"]))
            {
                $this->interpret = $opts["int-script"];
            }
            if(isset($opts["parse-only"]))
            {
                $this->parseonly = true;
            }
            if(isset($opts["int-only"]))
            {
                $this->intonly = true;
            }

        }
        elseif($argc > 2)
        {
            if(isset($opts["parse-only"]) && isset($opts["int-only"]))
            {
                self::errorMessage("parse-only and int-only can´t be combinated",10);
            }
            if(isset($opts["parse-only"]) && isset($opts["int-script"]))
            {
                self::errorMessage("parse-only and int-script can´t be combinated",10);
            }
            if(isset($opts["int-only"]) && isset($opts["parse-only"]))
            {
                self::errorMessage("int-only and parse-only can´t be combinated",10);
            }
            if(isset($opts["int-only"]) && isset($opts["parse-script"]))
            {
                self::errorMessage("int-only and parse-script can´t be combinated",10);
            }
            if(isset($opts["directory"]))
            {
                if(!is_dir($opts["directory"]))
                {
                    self::errorMessage("Specified directory is not a directory",11);
                }
                $this->directory = realpath($opts["directory"])."/";

            }
            if(isset($opts["recursive"]))
            {
                $this->recursive = true;
            }
            if(isset($opts["parse-script"]))
            {
                $this->parser = $opts["parse-script"];
            }
            if(isset($opts["int-script"]))
            {
                $this->interpret = $opts["int-script"];
            }
            if(isset($opts["parse-only"]))
            {
                $this->parseonly = true;
            }
            if(isset($opts["int-only"]))
            {
                $this->intonly = true;
            }
        }
    }

    public function checkFileExists()
    {
        if(!file_exists($this->interpret))
        {
            self::errorMessage("Input file interpret.py doesn´t exists",11);
        }
        if(!file_exists($this->parser))
        {
            self::errorMessage("Input file parse.php doesn´t exists",11);
        }
        if(!is_dir($this->directory))
        {
            self::errorMessage("Specified directory is not a directory",11);
        }

    }

    public static function showHelp()
    {
        echo "\n**********************************HELP**************************************************************************\n";
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

class Test extends CheckArgumentsAndError
{
    public $tests = array();

    public function runTest()
    {
        $in = false;
        $out = false;
        $rc = false;
        $tests;
        CheckArgumentsAndError::parseArguments($GLOBALS["argv"],$GLOBALS["argc"]);
        self::recursive($this->directory);
        //var_dump($this->tests);
        foreach($this->tests as $files)
        {
            $daco = pathinfo($files);
            if($files == $daco["filename"].".in")
            {
                $in = true;
            }
            if($files == $daco["filename"].".out")
            {
                $out = true;
            }
            if($files == $daco["filename"].".rc")
            {
                $rc = true;
            }
//////////// VYTVARANIE ////////////////
            if($in == false)
            {
                exec("touch ". $daco["dirname"] . "/". $daco["filename"].".in",$output,$return_var);
                if($return_var == 1)
                {
                    CheckArgumentsAndError::errorMessage("Couldn´t generate .in file",12);
                }
            }
            if($out == false)
            {
                exec("touch ". $daco["dirname"] . "/". $daco["filename"].".out",$output,$return_var);
                if($return_var == 1)
                {
                    CheckArgumentsAndError::errorMessage("Couldn´t generate .out file",12);
                }
            }
            if($rc == false)
            {
                exec("touch ". $daco["dirname"] . "/". $daco["filename"].".rc",$output,$return_var); //aby sme mohli skontrolovat ci sa vie vygenerovat alebo nie output tam musi byt neni to nic a return var tam je ta navratova hodnota
                exec("echo 0 >>" .  $daco["dirname"]."/".$daco["filename"].".rc");
                if($return_var == 1)
                {
                    CheckArgumentsAndError::errorMessage("Couldn´t generate .rc file",12);
                }
            }

        //////////////////////////////////////START TESTING /////////////////////////////////////////////////////////////////////////////////////////////////////////
        ////////// PARSE ONLY ////////////////////////
            exec("touch ./tempfileparse",$output,$return_var);
            if($return_var == 1)
            {
                CheckArgumentsAndError::errorMessage("Couldn´t make temporary file for parse",12);
            }
            exec("touch ./tempfileint",$output,$return_var);
            if($return_var == 1)
            {
                CheckArgumentsAndError::errorMessage("Couldn´t make temporary file for interpret",12);
            }
            exec("touch ./tempfileboth",$output,$return_var);
            if($return_var == 1)
            {
                CheckArgumentsAndError::errorMessage("Couldn´t make temporary file for both parse and interpret",12);
            }
            $rc = file_get_contents($daco["dirname"]."/".$daco["filename"].".rc"); // nacitanie obsahu rc

            if($this->parseonly == true)
            {
                exec("php7.3 ".$this->parser. "< ".$daco["dirname"]."/".$daco["filename"].".src > ./tempfileparse",$output,$ret_parse);
                if($rc == $ret_parse)
                {
                    exec("java -jar /pub/courses/ipp/jexamxml/jexamxml.jar tempfileparse ".$daco["dirname"]."/".$daco["filename"].".out /pub/courses/ipp/jexamxml/options",$output,$ret_parse);
                    if($ret_parse == 0)
                    {
                        print("ok\n");
                    }
                    else
                    {
                        print("Chyba v teste ".$daco["basename"]."\n");
                    }
                }
                else
                {
                    print($daco["basename"].":neni ok nerovnaju sa rc\n");
                }
            }
            elseif($this->intonly == true)
            {
                exec("python3.6".$this->interpret. "--source=".$daco["dirname"]."/". "--input=".$daco["dirname"]."/".$daco["filename"]. ".in > ./tempfileint",$output,$rc_return_var);
                if($rc == $rc_return_var)
                {
                    exec("diff ". $daco["dirname"]."/".$daco["filename"].".out tempfileint",$output,$diff_ret);
                    if($diff_ret == 0)
                        print("ok");
                    else
                    {
                        print("neni ok neni su rovnake");
                    }
                }
                else
                {
                    print("test nepresiel nerovnaju sa rc");
                }
            }
            else
            {
                exec("php7.3 ".$this->parser. "< ".$daco["dirname"]."/".".src > ./tempfileboth");
                exec("python3.6".$this->interpret. "--source=".$daco["dirname"]."/". "--input=".$daco["dirname"]."/".$daco["filename"]. ".in > ./tempfileboth",$output,$rc_return_var);
                if($rc == $rc_return_var)
                {
                    exec("diff ". $daco["dirname"].$daco["filename"]."/".".out tempfileboth",$output,$diff_ret);
                    if($diff_ret == 0)
                        print("ok");
                    else
                    {
                        print("neni ok neni su rovnake");
                    }
                }
                else
                {
                    print("test nepresiel nerovnaju sa rc");
                }
            }
        }
            exec("rm -rf ./tempfileparse");
            exec("rm -rf ./tempfileint");
            exec("rm -rf ./tempfileboth");
    }


    public function recursive($dir)
    {
        $files = scandir($dir);
        foreach($files as $file)
        {
            $file = $dir.$file; // cesta skonkatenovana s nazvom file a je to ulozene do file
            if(is_dir($file)) //ak je priecinok ten file s celou cestou a je nastavena rekurzia tak preskoc . a .. a rekurzivne zavolaj funkciu
            {
                if($this->recursive == true)
                {
                    if($file == $dir."." || $file == $dir."..")
                        continue;
                    self::recursive($file ."/");
                }
            }
            else
            {
                array_push($this->tests,$file); // do pola ulozime vsetky subory ktore niesu dir
            }
        }
    }
}





/*class HTMLgen
{
    public function generateHtmlPage()
    {
          // Tu bude HTML kod

    }
}*/
$Argument = new CheckArgumentsAndError();
//$Argument->parseArguments($argc,$argv);
$Argument->checkFileExists();
//$HtmlGenerator = new HTMLgen
//$HtmlGenerator->generateHtmlPage();
$test = new Test();
$test->runTest();

 ?>
