from Parser.parser import Parser
from Parser.exceptions import InvalidSyntax
import os

if __name__ == '__main__':
    myParser = Parser('ASMFiles/P7.asm' if os.name == 'posix' else 'ASMFiles\P7.asm','P7.o')
    myParser.run()
