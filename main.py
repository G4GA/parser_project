from Parser.parser import Parser
from Parser.exceptions import InvalidSyntax
import os

if __name__ == '__main__':
    filepath = 'ASMFiles/P8.asm' if os.name == 'posix' else 'ASMFiles\P8.asm'
    myParser = Parser(filepath,'P8.o')
    myParser.run()
