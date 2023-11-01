from Parser.parser import Parser
from Parser.exceptions import InvalidSyntax
import sys

if __name__ == '__main__':
    myParser = Parser('ASMFiles\P4.asm')
    myParser.run()
