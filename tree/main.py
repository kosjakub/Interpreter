import sys
import pprint
import Mparser
import sys
import ply.lex as lex
import scanner
import TreePrinter

if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = Mparser.parser
    text = file.read()
    lexer = scanner.lexer
    t = parser.parse(text, lexer=lexer)
    t.printTree()
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(t)