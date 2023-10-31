from Utilities import error_codes as e_cds
from Utilities.casting import stov
from Utilities import files
from Utilities import mnemonics

class Parser:
    def __init__ (self,file_path):
        self.asm_lines = []
        self.code_str = ''
        self.operation_lines = []

    def run (self):
        self.load_file("P4.asm")
        self.parse_line()

    def parse_line (self):
        asm_line = self.asm_lines.pop(0).lstrip().split(' ')
        print(asm_line)


    def load_file (self, path:str):
        with open(path,'r',encoding='utf-8') as file:
            self.code_str = file.read()
        self.asm_lines = self.code_str.splitlines()


    def write_file (self, path:str):
        pass