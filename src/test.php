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

    public function parseArguments($argc,$argv)
    {

        $options = array("help","directory::","recursive","parse-script::","int-script::","parse-only","int-only");
        $opts = getopt("",$options);
        if($argc === 2)
        {
            if(isset($opts["help"]))
            {
                if($argv[1] === "--help")
                {
                    self::showHelp();
                }
            }
            elseif(isset($opts["directory"]))
            {
                if(!is_dir($opts["directory"]))
                {
                    self::errorMessage("Specified directory is not a directory",11);
                }
                $this->directory = realpath($opts["directory"])."/";
                print("riadok 57");
                var_dump($this->directory);

            }
            elseif(isset($opts["recursive"]))
            {
                $this->recursive = true;
            }
            elseif(isset($opts["parse-script"]))
            {
                $this->parser = $opts["parse-script"];
            }
            elseif(isset($opts["int-script"]))
            {
                $this->interpret = $opts["int-script"];
            }
            elseif(isset($opts["parse-only"]))
            {
                $this->parseonly = true;
            }
            elseif(isset($opts["int-only"]))
            {
                $this->intonly = true;
            }
            else
            {
                self::errorMessage("Bad arguments",10);
            }
        }
        if($argc > 2)
        {
            if(isset($opts["parse-only"]) && isset($opts["int-only"]))
            {
                self::errorMessage("parse-only and int-only can´t be combinated",10);
            }
            elseif(isset($opts["parse-only"]) && isset($opts["int-script"]))
            {
                self::errorMessage("parse-only and int-script can´t be combinated",10);
            }
            elseif(isset($opts["int-only"]) && isset($opts["parse-only"]))
            {
                self::errorMessage("int-only and parse-only can´t be combinated",10);
            }
            elseif(isset($opts["int-only"]) && isset($opts["parse-script"]))
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
                print("riadok 110");
                var_dump($this->directory);
            }
            elseif(isset($opts["recursive"]))
            {
                $this->recursive = true;
            }
            elseif(isset($opts["parse-script"]))
            {
                $this->parser = $opts["parse-script"];
            }
            elseif(isset($opts["int-script"]))
            {
                $this->interpret = $opts["int-script"];
            }
            elseif(isset($opts["parse-only"]))
            {
                $this->parseonly = true;
            }
            elseif(isset($opts["int-only"]))
            {
                $this->intonly = true;
            }
            else
            {
                self::errorMessage("Bad arguments",10);
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

    public function runTest()
    {
        CheckArgumentsAndError::parseArguments($GLOBALS["argv"],$GLOBALS["argc"]);
        $files = scandir($this->directory);
        var_dump($this->directory);
        var_dump($files);
        $base = basename($this->directory);
        var_dump($this->directory);
        foreach($files as $file)
        {
            if(is_dir($this->directory.$file))
            {
                if($this->recursive == true)
                    if($file == "." || $file == "..")
                    continue;
                    self::runTest($this->directory . $file . "/");
            }
                else
                {
                    continue;
                }
        }
        var_dump($files);

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
