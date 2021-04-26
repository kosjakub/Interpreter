import sys
import pprint
import Mparser
import sys
import ply.lex as lex
import scanner
import TreePrinter
from TypeChecker import TypeChecker

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
    typeChecker = TypeChecker()   
       # or alternatively ast.accept(typeChecker)
    for x in t:
        typeChecker.visit(x)

    # for x in t:
    #     x.printTree()

    #print(t)
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(t)