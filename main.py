from Parser.parser import Parser
from Parser.exceptions import InvalidSyntax
import os

if __name__ == '__main__':
    filepath = 'ASMFiles/P9.asm' if os.name == 'posix' else 'ASMFiles\P9.asm'
    myParser = Parser(filepath,'P9.o')
    myParser.run()
