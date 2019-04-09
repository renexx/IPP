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
                $this->parser = realpath($opts["parse-script"]);
            }
            if(isset($opts["int-script"]))
            {
                $this->interpret = realpath($opts["int-script"]);
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

                if(!is_dir(realpath($opts["directory"])))
                {
                    self::errorMessage("Specified directory is not a real directory",11);
                }
                $this->directory = realpath($opts["directory"])."/";

            }
            if(isset($opts["recursive"]))
            {
                $this->recursive = true;
            }
            if(isset($opts["parse-script"]))
            {
                $this->parser = realpath($opts["parse-script"]);
            }
            if(isset($opts["int-script"]))
            {
                $this->interpret = realpath($opts["int-script"]);
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
        if($this->intonly)
        {
            if(!file_exists($this->interpret))
            {
                self::errorMessage("Input file interpret.py doesn´t exists",11);
            }

        }
        elseif($this->parseonly)
        {
            if(!file_exists($this->parser))
            {
                self::errorMessage("Input file parse.php doesn´t exists",11);
            }
        }
        else
        {
            if(!file_exists($this->interpret))
            {
                self::errorMessage("Input file interpret.py doesn´t exists",11);
            }
            if(!file_exists($this->parser))
            {
                self::errorMessage("Input file parse.php doesn´t exists",11);
            }

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
    public $testCounter = 0;
    public $testPassed = 0;
    public $testFail = 0;
    public $passedarray = array();

    public function runTest()
    {
        $in = false;
        $out = false;
        $rc = false;
        $tests;
        $passedarray;
        CheckArgumentsAndError::parseArguments($GLOBALS["argv"],$GLOBALS["argc"]);
        CheckArgumentsAndError::checkFileExists();
        self::recursive($this->directory);
        $this->testCounter;
        $oldpath = "";
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
                exec("echo 0 >" .  $daco["dirname"]."/".$daco["filename"].".rc");
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
            exec("touch ./tempoutput",$output,$return_var);
            if($return_var == 1)
            {
                CheckArgumentsAndError::errorMessage("Couldn´t make temporary file for both parse and interpret",12);
            }

            $rc = file_get_contents($daco["dirname"]."/".$daco["filename"].".rc"); // nacitanie obsahu rc

            if($daco["basename"] == $daco["filename"].".src")
            {
                if($daco["dirname"] != $oldpath)
                {
                    echo "\n
                        <div><br>
                          <br>
                          <section>
                              <h3>FOLDER: <strong>".$daco["dirname"]."</strong></h3>
                              <br>
                          </section>
                        </div>\n";
                        $oldpath = $daco["dirname"];
                }
                //echo "<br><br><br><font size=\"2\" color=\"black\">Test #" . $this->testCounter . " </font><br>";
                if($this->parseonly == true)
                {
                    exec("php7.3 ".$this->parser. "< \"".$daco["dirname"]."/".$daco["filename"].".src\" > ./tempfileparse",$output,$ret_parse);
                    if($rc == $ret_parse)
                    {
                        exec("java -jar /pub/courses/ipp/jexamxml/jexamxml.jar tempfileparse \"".$daco["dirname"]."/".$daco["filename"].".out\" /pub/courses/ipp/jexamxml/options",$output,$ret_parse);
                        if($ret_parse == 0)
                        {
                            echo "<font size=\"5\" color=\"green\">PASSED: TEST JEXAMXML:\t\t <strong>".$daco["basename"]."</strong></font><br>";

                            $this->testPassed++;

                        }
                        else
                        {
                            echo "<font size=\"5\" color=\"green\">FAILED: TEST JEXAMXML:\t\t <strong>".$daco["basename"]."</strong></font><br>";
                            $this->testFail++;

                        }
                    }
                    else
                    {
                        echo "<font size=\"5\" color=\"red\">FAILED: TEST RC:\t\t <strong>".$daco["basename"]."</strong><strong>  (expected RC should be :".$rc." real RC is: ".$ret_parse.")</strong> </font><br>";
                        $this->testFail++;
                    }
                }
                elseif($this->intonly == true)
                {
                    exec("python3 ".$this->interpret. " --source=\"".$daco["dirname"]."/".$daco["filename"].".src\"  --input=\"".$daco["dirname"]."/".$daco["filename"].".in\" > ./tempfileint",$output,$rc_return_var);
                    if($rc == $rc_return_var)
                    {
                        exec("diff \"".$daco["dirname"]."/".$daco["filename"].".out\" tempfileint",$output,$diff_ret);
                        if($diff_ret == 0)
                        {
                            echo "<font size=\"5\" color=\"green\">PASSED: TEST DIFF:\t\t <strong>".$daco["basename"]."</strong></font><br>";
                            $this->testPassed++;
                        }
                        else
                        {
                            echo "<font size=\"5\" color=\"red\">FAILED: TEST DIFF:\t\t <strong>".$daco["basename"]."</strong></font><br>";
                            $this->testFail++;
                        }
                    }
                    else
                    {
                        echo "<font size=\"5\" color=\"red\">FAILED: TEST RC:\t\t <strong>".$daco["basename"]."</strong><strong>  (expected RC should be :".$rc."  real RC is: ".$rc_return_var.")</strong> </font><br>";
                        $this->testFail++;
                    }
                }
                else
                {
                    exec("php7.3 ".$this->parser. "< \"".$daco["dirname"]."/".$daco["filename"].".src\" > ./tempfileboth");
                    exec("python3.6 ".$this->interpret. " --source=\"./tempfileboth\"  --input=\"".$daco["dirname"]."/".$daco["filename"].".in\" > ./tempoutput",$output,$rc_return_var);
                    if($rc == $rc_return_var)
                    {
                        exec("diff \"".$daco["dirname"]."/".$daco["filename"].".out\" tempoutput",$output,$diff_ret);
                        if($diff_ret == 0)
                        {

                            echo "<font size=\"5\" color=\"green\">PASSED: TEST DIFF:\t\t <strong>".$daco["basename"]."</strong></font><br>";
                            $this->testPassed++;
                        }
                        else
                        {
                            echo "<font size=\"5\" color=\"red\">FAILED: TEST DIFF:\t\t <strong>".$daco["basename"]."</strong></font><br>";
                            $this->testFail++;
                        }
                    }
                    else
                    {
                        echo "<font size=\"5\" color=\"red\">FAILED: TEST RC:\t\t <strong>".$daco["basename"]."</strong><strong>  (expected RC should be :".$rc."  real RC is : ".$rc_return_var.")</strong> </font><br>";
                        $this->testFail++;
                    }
                }
                $this->testCounter++;
            }
        }
            exec("rm -rf ./tempfileparse");
            exec("rm -rf ./tempfileint");
            exec("rm -rf ./tempfileboth");
            exec("rm -rf ./tempoutput");

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
    public function printTest()
    {

    }
}





class Htmlgen extends Test
{
    public function generateHtmlPage()
    {
        echo "<!DOCTYPE html>
    <html>
      <head>
        <style>
          body {
            font-size: 14px;
            padding-top: 0%;
            text-align: left;
            font: 14px Verdana;
            color: white;
            background-color: #101111;
            padding-left: 40px;
          }
          h1
          {
              font-size: 2em;
              font-weight: normal;
              color: white;
              text-align: center;
              text-shadow: 2px 2px 1px #0a294b;
          }
          h2 {
            text-align: left;
            color: white;
            font-family: Arial;
            text-shadow: 3px 3px 7px #0a294b;
          }
          h3
          {
              text-align: left;
              color: white;
              font-family: 'monospaced', monospace;

          }
          table, th, td {
              border: 1px solid white;
              border-collapse: collapse;
            }
            th, td {
              padding: 5px;
              text-align: center;

            }
            table{
                width:50%;
            }
            caption{
                text-align:left;
                font-family: Arial;
                text-shadow: 3px 3px 7px #0a294b;
                color: #white;
                font-size: 1.5em;
                font-weight: bold;
                padding-bottom: 10px;

            }

            article
            {
                padding: 30px 0px;
            }

        </style>
      </head>
      <body>
        <article>
            <h1>TEST SUMMARY FOR IPPCODE19 </h1>\n";
            if ($this->parseonly == true) {
                echo "\n
            <div>
              MODE: <h2<strong>parse-only</strong><br><br></h2>
            </div>\n";
        } elseif ($this->intonly == true) {
                echo "\n
            <div>
              MODE: <h2><strong>int-only</strong><br><br></h2>
            </div>\n";
            } else {
                echo "\n
            <div>
                <h2>MODE: <strong>BOTH (INTERPRET, PARSER)</strong><br><br></h2>
            </div>\n";
            }
            Test::runTest();
            echo "\n
            <div>
                <br><br>

                    <table>
                    <caption>RESULT</caption>
                      <tr>
                        <th>ALL</th>
                        <th>FAILED</th>
                        <th>PASSED</th>
                      </tr>
                      <tr>
                        <td><font size =\"3\" color=\"white\"<strong>".$this->testCounter."</strong></td>
                        <td><font size=\"3\" color=\"red\"><strong>".$this->testFail."</strong></font></td>
                        <td><font size=\"3\" color=\"green\"><strong>".$this->testPassed."</strong></font></td>
                      </tr>
                    </table>

            </div>
        </article>
          </body>
    </html>\n";
    }

    }

$Argument = new CheckArgumentsAndError();
//$Argument->parseArguments($argc,$argv);
$test = new Test();
$HtmlGenerator = new Htmlgen;
$HtmlGenerator->generateHtmlPage();

 ?>
