import ctypes
from exceptions import InvalidSyntax
from Utilities import error_codes as e_cds
from Utilities.casting import stov
from Utilities import files
from Utilities import mnemonics

class Parser:
    def __init__ (self,file_path):
        self._asm_lines = []
        self._code_str = ''
        self._current = 0
        self._labels = []
        self._operation_lines = []

    def run (self):
        self.load_file("P4.asm")
        self.parse_line()

    def parse_line (self):
        asm_line = self.asm_lines.pop(0).lstrip().split(' ')
        op_code = ''
        try:
            if (asm_line[0] == 'ORG'):
                self.current = stov(asm_line[1])
            else:
                monic = mnemonics.match(asm_line[0])
                if (monic is None):
                    asm_line = self.label(asm_line)
                if (asm_line):
                    op_code = self.get_op_code(asm_line,monic)
        except IndexError:
            raise InvalidSyntax('Missing arguments',self.current)
        except IndentationError or ValueError:
            raise InvalidSyntax('Invalid number',self.curent)

    def get_op_code(self,asm_line,monic):
        pass

    def get_addr_mode (self,asm_line,monic):
        pass


    def label(self,asm_line):
        try:
            if (asm_line[1] == 'EQU'):
                self.labels.append({asm_line[0]:int(stov(asm_line[2]))})
                asm_line.clear()

            elif (asm_line[1] == 'END'):
                self.labels.append({asm_line[0]:self.current})
                asm_line.clear()

            elif (mnemonics.match(asm_line[1]) is not None):
                self.labels.append({asm_line[0]:self.current})
                asm_line.pop(0)

            else:
                raise InvalidSyntax('Invalid arguments',self)

        except IndexError as err:
            raise InvalidSyntax('Missing arguments',self.current)
        except IndentationError or ValueError:
            raise InvalidSyntax('Invalid number',self.current)

        return asm_line


    def load_file (self, path:str):
        with open(path,'r',encoding='utf-8') as file:
            self.code_str = file.read()
        self.asm_lines = self.code_str.splitlines()

    @property
    def code_str (self):
        return


    def write_file (self, path:str):
        pass