<?php
/**
 * Project: Project for Principles of Programming Languages subject
 * @file test.php
 * @brief This script launches tests for parse.php and interpret.py
 * @author René Bolf <xbolfr00@stud.fit.vutbr.cz>
 */
 /**
  * @class CheckArgumentsAndError
  * @brief This is class for check arguments, help, errorMessage, check existence of file
  * @attrib - public $recursive - for parameter --recursive
  * @attrib - public $directory - for parameter --directory=path
  * @attrib - public $interpret - for parameter --int-script=file
  * @attrib - public $parser - for parameter --parse-script=file
  * @attrib - public $parseonly - for paramter --parse-only
  * @attrib - public $intonly - for parameter --int-only
  */
class CheckArgumentsAndError
{

    public $recursive;
    public $directory;
    public $parser;
    public $interpret;
    public $parseonly;
    public $intonly;

    /**
     * @brief Constructor for set attributes
     */
    public function __construct()
    {
        $this->recursive = false;
        $this->parser = realpath("./parse.php"); /*realpath find real path*/
        $this->interpret = realpath("./interpret.py");
        $this->parseonly = false;
        $this->intonly = false;
        $this->directory = realpath("./");
        if(!is_dir($this->directory))
        {
            self::errorMessage("Specified directory is not a directory",11);
        }
        $this->directory = $this->directory."/"; //have to be concat with / for right path
    }
    /**
     * @brief Method parseArguments, for parse and check arguments
     * @param $argc
     * @param $argv
     */
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
    /**
     * @brief Method checkFileExists, check the existence of a file
     */
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
    /**
     * @brief Method show help, for printing help
     */
    public static function showHelp()
    {
        echo "\n**********************************HELP************************************************************************************************************************************************\n";
        echo "HELP : --help\t print help\n";
        echo "test.php - This script is for automatic tests for parse.php and interpret.py\n";
        echo "This script scans the specified directory with tests and will uses them for automatically test for functionality both files(parse.php,interpret.py) result will be printed in HTML 5\n";
        echo "\n******************************HOW TO RUN *********************************************************************************************************************************************\n";
        echo "\n--help - print help";
        echo "--directory=path -- the tests will search in the specified direcotry (if this parameter is missing, script scans actual direcotry)\n";
        echo "--recursive - tests will be looking for not only in specified directory, but also recursively in all subdirectory\n";
        echo "--parse-script=file - file with script in PHP7.3 for analysis source code in IPPcode19(if this parameter is missing, so implicity vaulue is parse.php (in acutal direcotry) )\n";
        echo "--int-script=file file with script in python 3.6 for interpreting XML code in IPPCODE19(if this parameter is missing, implicity value is interpret.py (in acutal directory))\n";
        echo "--parse-only - test only parse.php\n";
        echo "--int-only - test only interpret.py\n";
        echo "--parse-only can´t be combinated with --int-only and --int-script\n";
        echo "--int-only can´t be combinated with --parse-only and --parse-script\n";
        exit(0);
    }
    /**
     * @brief Method errorMessage this method write to the STDERR error message and error code
     * @param $message is a message for error code
     * @param $exitCode is error code
     */
    public static function errorMessage($message,$exitCode)
    {
        fclose(STDIN);
        $message .= "\n";
        fwrite(STDERR,$message);
        exit($exitCode);
    }
}
/**
 * @class Test inherit from class CheckArgumentsAndError (attributes,methods)
 * @attrib $tests = array() array of tests
 * @attrib $testCounter = 0 is a test counter this is for results how many tests have been done
 * @attrib $testPassed = 0 is a test passed counter this is for result how many tests are passed
 * @attrib $testFail = 0 is a test failed cunter this is for result how many tests are failed
  *@attrib $passedarray = array() is a array of passed tests
 */
class Test extends CheckArgumentsAndError
{
    public $tests = array();
    public $testCounter = 0;
    public $testPassed = 0;
    public $testFail = 0;
    public $passedarray = array();

    /**
     * @brief Method runTest, is  for  executing tests
     */
    public function runTest()
    {
        $in = false; /** file .in **/
        $out = false; /*file .out */
        $rc = false; /*file . rc */
        $tests;
        $passedarray;
        CheckArgumentsAndError::parseArguments($GLOBALS["argv"],$GLOBALS["argc"]);
        CheckArgumentsAndError::checkFileExists();
        self::recursive($this->directory);
        $this->testCounter;
        $oldpath = "";
        foreach($this->tests as $files)
        {
            $path = pathinfo($files);
            if($files == $path["filename"].".in")
            {
                $in = true;
            }
            if($files == $path["filename"].".out")
            {
                $out = true;
            }
            if($files == $path["filename"].".rc")
            {
                $rc = true;
            }
/**************************************** Make files  *****************************************************/
            if($in == false)
            {
                exec("touch ". $path["dirname"] . "/". $path["filename"].".in",$output,$return_var);
                if($return_var == 1)
                {
                    CheckArgumentsAndError::errorMessage("Couldn´t generate .in file",12);
                }
            }
            if($out == false)
            {
                exec("touch ". $path["dirname"] . "/". $path["filename"].".out",$output,$return_var);
                if($return_var == 1)
                {
                    CheckArgumentsAndError::errorMessage("Couldn´t generate .out file",12);
                }
            }
            if($rc == false)
            {
                exec("touch ". $path["dirname"] . "/". $path["filename"].".rc",$output,$return_var); // for check, $output have to be here(nothing) $return_var contain return value
                exec("echo 0 >" .  $path["dirname"]."/".$path["filename"].".rc");
                if($return_var == 1)
                {
                    CheckArgumentsAndError::errorMessage("Couldn´t generate .rc file",12);
                }
            }

/******************************************START TESTING ********************************************************************/
/******************************************* PARSE ONLY *********************************************************************/
            exec("touch ./tempfileparse",$output,$return_var); /*make temporary file for parse tests */
            if($return_var == 1)
            {
                CheckArgumentsAndError::errorMessage("Couldn´t make temporary file for parse",12);
            }
            exec("touch ./tempfileint",$output,$return_var); /*make temporary file for interpret*/
            if($return_var == 1)
            {
                CheckArgumentsAndError::errorMessage("Couldn´t make temporary file for interpret",12);
            }
            exec("touch ./tempfileboth",$output,$return_var); /*maek temporary file for both*/
            if($return_var == 1)
            {
                CheckArgumentsAndError::errorMessage("Couldn´t make temporary file for both parse and interpret",12);
            }
            exec("touch ./tempoutput",$output,$return_var); /*make temp file for output in both tests*/
            if($return_var == 1)
            {
                CheckArgumentsAndError::errorMessage("Couldn´t make temporary file for both parse and interpret",12);
            }
            exec("touch ./templog",$output,$return_var); /*for jexamxml*/
            if($return_var == 1)
            {
                CheckArgumentsAndError::errorMessage("Couldn´t make temporary file for both parse and interpret",12);
            }

            $rc = file_get_contents($path["dirname"]."/".$path["filename"].".rc"); /*for get contents from rc files*/

            if($path["basename"] == $path["filename"].".src")
            {
                if($path["dirname"] != $oldpath)
                {
                    echo "\n
                        <div><br>
                          <br>
                          <section>
                              <h3>FOLDER: <strong>".$path["dirname"]."</strong></h3>
                              <br>
                          </section>
                        </div>\n";
                        $oldpath = $path["dirname"];
                }
/******************************** PARE ONLY ******************************************************************/
                if($this->parseonly == true)
                {
                    exec("php7.3 ".$this->parser. "< \"".$path["dirname"]."/".$path["filename"].".src\" > ./tempfileparse 2>/dev/null",$output,$ret_parse); /*2>/dev/null redirection error message*/
                    if($rc == $ret_parse)
                    {
                        if($ret_parse != 0)
                        {
                            $ret_parse = 0;
                        }
                        else
                        {
                            exec("java -jar /pub/courses/ipp/jexamxml/jexamxml.jar tempfileparse \"".$path["dirname"]."/".$path["filename"].".out\" templog /D /pub/courses/ipp/jexamxml/options",$output,$ret_parse);
                        }
                        if($ret_parse == 0)
                        {
                            echo "<font size=\"5\" color=\"green\">PASSED: TEST JEXAMXML:\t\t <strong>".$path["basename"]."</strong></font><br>";

                            $this->testPassed++;

                        }
                        else
                        {
                            echo "<font size=\"5\" color=\"green\">FAILED: TEST JEXAMXML:\t\t <strong>".$path["basename"]."</strong></font><br>";
                            $this->testFail++;

                        }
                    }
                    else
                    {
                        echo "<font size=\"5\" color=\"red\">FAILED: TEST RC:\t\t <strong>".$path["basename"]."</strong><strong>  (expected RC should be :".$rc." real RC is: ".$ret_parse.")</strong> </font><br>";
                        $this->testFail++;
                    }
                }
/**************************************************** INTERPRET ONLY *******************************************/
                elseif($this->intonly == true)
                {
                    exec("python3 ".$this->interpret. " --source=\"".$path["dirname"]."/".$path["filename"].".src\"  --input=\"".$path["dirname"]."/".$path["filename"].".in\" > ./tempfileint 2>/dev/null",$output,$rc_return_var);
                    if($rc == $rc_return_var)
                    {
                        if($rc_return_var != 0)
                        {
                            $diff_ret = 0;
                        }
                        else
                        {
                            exec("diff \"".$path["dirname"]."/".$path["filename"].".out\" tempfileint",$output,$diff_ret);
                        }
                        if($diff_ret == 0)
                        {
                            echo "<font size=\"5\" color=\"green\">PASSED: TEST DIFF:\t\t <strong>".$path["basename"]."</strong></font><br>";
                            $this->testPassed++;
                        }
                        else
                        {
                            echo "<font size=\"5\" color=\"red\">FAILED: TEST DIFF:\t\t <strong>".$path["basename"]."</strong></font><br>";
                            $this->testFail++;
                        }
                    }
                    else
                    {
                        echo "<font size=\"5\" color=\"red\">FAILED: TEST RC:\t\t <strong>".$path["basename"]."</strong><strong>  (expected RC should be :".$rc."  real RC is: ".$rc_return_var.")</strong> </font><br>";
                        $this->testFail++;
                    }
                }
/**************************************** BOTH (PARSER,INTERPRET) *****************************************************/
                else
                {
                    exec("php7.3 ".$this->parser. "< \"".$path["dirname"]."/".$path["filename"].".src\" > ./tempfileboth 2>/dev/null");
                    exec("python3.6 ".$this->interpret. " --source=\"./tempfileboth\"  --input=\"".$path["dirname"]."/".$path["filename"].".in\" > ./tempoutput 2>/dev/null",$output,$rc_return_var);
                    if($rc == $rc_return_var)
                    {
                        if($rc_return_var != 0)
                        {
                            $diff_ret = 0;
                        }
                        else
                        {
                            exec("diff \"".$path["dirname"]."/".$path["filename"].".out\" tempoutput",$output,$diff_ret);
                        }
                        if($diff_ret == 0)
                        {

                            echo "<font size=\"5\" color=\"green\">PASSED: TEST DIFF:\t\t <strong>".$path["basename"]."</strong></font><br>";
                            $this->testPassed++;
                        }
                        else
                        {
                            echo "<font size=\"5\" color=\"red\">FAILED: TEST DIFF:\t\t <strong>".$path["basename"]."</strong></font><br>";
                            $this->testFail++;
                        }
                    }
                    else
                    {
                        echo "<font size=\"5\" color=\"red\">FAILED: TEST RC:\t\t <strong>".$path["basename"]."</strong><strong>  (expected RC should be :".$rc."  real RC is : ".$rc_return_var.")</strong> </font><br>";
                        $this->testFail++;
                    }
                }
                $this->testCounter++;
            }
        }
/************** DELETE temp FILES ****************************************/
            exec("rm -rf ./tempfileparse");
            exec("rm -rf ./tempfileint");
            exec("rm -rf ./tempfileboth");
            exec("rm -rf ./tempoutput");
            exec("rm -rf ./templog");
    }

    /**
     * @brief Method recursove, is  for  recursive search in directory
     */
    public function recursive($dir)
    {
        $files = scandir($dir);
        foreach($files as $file)
        {
            $file = $dir.$file; /* path contacted with name and save in to $file */
            if(is_dir($file)) /* if is direcotry this file with all path and is set recursive paramter then skip and recursively call function*/
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
                array_push($this->tests,$file); // In to the array save all files which not dir */
            }
        }
    }
}



/**
 * @classs HTmlgen is a class for generate html and this class inherit from class Test
 */


class Htmlgen extends Test
{
    /**
     * @brief method generateHtmlPage this method generate html in to the stdout
     *
     */

    public function generateHtmlPage()
    {
        echo "<!DOCTYPE html>
    <html>
      <head>
          <meta charset=\"utf-8\" />
          <title>Test summary for ippcode19</title>
      </head>
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
                padding-bottom: 10px;
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
      <body>
        <article>
            <h1>TEST SUMMARY FOR IPPCODE19 </h1>\n";
            Test::runTest();
            echo "\n
            <div>
                <br><br>
                    <table>
                    <caption>";
                    if ($this->parseonly == true) {
                        echo "\n
                    <div>
                      RESULT MODE: <strong>parse-only</strong>
                    </div>\n";
                } elseif ($this->intonly == true) {
                        echo "\n
                    <div>
                      RESULT MODE: <strong>int-only</strong>
                    </div>\n";
                    } else {
                        echo "\n
                    <div>
                        RESULT MODE: <strong>BOTH (INTERPRET, PARSER)</strong>
                    </div>\n";
                    }
                    echo "
                    </caption>
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
$test = new Test();
$HtmlGenerator = new Htmlgen;
$HtmlGenerator->generateHtmlPage();

 ?>
