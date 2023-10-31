from Parser.parser import Parser
from Parser.exceptions import InvalidSyntax
import sys

if __name__ == '__main__':
    myParser = Parser('P4.asm')
    try:
        myParser.run()
    except InvalidSyntax as Ins:
        print(Ins)
        sys._ExitCode = 1
        sys.exit()