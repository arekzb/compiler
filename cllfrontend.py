import cllcompiler
import getopt
import sys

class CllCompilerFrontend:

    """Frontend wrapper for Ehtereum cllcompiler.

    Frontend wrapper around Ethereum compiler functions has the
    expected usage:

    Do not pass any parameters to the __init__method
    it is unimplemented

        cl = CllCompilerFrontend()

    Pass the list of arguments to parseArguments() method

        cl.parseOptions(sys.argv[1:])

    Call the main method run() without any arguments

        cl.run()

    Resulting steps are mostly outlined in run() method doctring
    as well as in the individual methods

    """
    input_file = ""
    output_file = "a.out"
    input_stream = []
    ast = False
    compiled_statements = []
    assembled_code = []
    msg = "Unknown error occurred"

    def __init__(self):
        """Constructor initializer

        Does nothing at the moment
        """
        pass

    def printHelp(self):
        """PrintHelp outputs current help and exits with status 2

        I show you what to do dude.
        """
        print "compiler.py -i inputfile -o outputfile"
        sys.exit(2)

    def parseOptions(self, argv):
        """Takes passed in options from the passed in arguments

        Expects to see options h, i, o.

        h prints help

        i sets the input file. Input file has no default value
            and as such, if it is unreadable, process will stop.

        o sets the output file. Output file has default value of a.out
        """
        try:
            opts, args = getopt.getopt(argv, "hi:o",["inputfile=","outputfile="])
        except getopt.GetoptError:
            self.printHelp()

        for opt, arg in opts:
            if opt == '-h':
                print "compiler.py -i inputfile -o outputfile"
                sys.exit(0)
            elif opt in ("-i", "--inputfile"):
                self.input_file = arg
            elif opt in ("-o", "--outputfile"):
                self.output_file = arg

        if self.input_file == "":
            self.printHelp()

    def terminate(self):
        """Terminates and prints current message, usually trapped Exception

        That's pretty much it
        """
        print self.msg
        sys.exit(2)

    def getInputFileContents(self):
        """Gets contents of a file

        Reads in the contents of the input file and stores
        each line as a value in input_stream array. On exception,
        msg is set to the trapped Exception and program terminates.
        """
        try:
            with open(self.input_file) as handle:
                self.input_stream = handle.readlines()
        except IOError as e:
            self.msg = e
            self.terminate()

    def parseInputStream(self):
        """Parses the input stream via cllcompiler

        Takes contents of array in input_stream and passes them
        to the cllcompiler.parse_lines(). Resulting AST array is
        stored in ast. On exception, msg is set to the trapped Exception
        and program terminates.
        """
        try:
            self.ast = cllcompiler.parse_lines(self.input_stream)
        except Exception as e:
            self.msg = e
            self.terminate()

    def compileStatements(self):
        """Compiles the AST via cllcompiler

        Calls cllcompiler.compile_stmt(), passes array ast
        and assigns return value to compiled_statements array.
        On exception, msg is set to the trapped Exception and
        program terminates.
        """
        try:
            self.compiled_statements = cllcompiler.compile_stmt(self.ast)
        except Exception as e:
            self.msg = e
            self.terminate()

    def assembleCode(self):
        """Assembles the compiled statements via cllcompiler

        Calls cllcompiler.assemble(), passes compiled_statements array
        and assigns return to assembled_code. On exception, msg is set
        to the trapped Exception and program terminates.
        """
        try:
            self.assembled_code = cllcompiler.assemble(self.compiled_statements)
        except Exception as e:
            self.msg = e
            self.terminate()

    def run(self):
        """Main method expected to be called by users.

        Reads in contents from the input file.
        Fills in the input_stream with lines from input file
        Squashes the input_stream array into a text string input_text
        Passes input_stream array to cllcompiler.parse_lines() which returns AST
            AST is stored in ast.
        Passes ast to to cllcompiler.compile_stmt() which returns an array of
            compiled statements, stored in compiled_statements.
        Passes compiled_statements to cllcompiler.assemble() which returns
            an array of ethereum Cll codes.

        At the end, this is just an 'unrolled' approach of the
            procedure done in originally released runtests
            example script, with added structured user land
            methods.
        """
        self.getInputFileContents()
        self.parseInputStream()
        self.compileStatements()
        self.assembleCode()

    def __str__(self):
        if len(self.assembled_code) > 0:
            return " ".join(str(c) for c in self.assembled_code)
        else:
            return "No generated code from %s" % (self.input_file)
