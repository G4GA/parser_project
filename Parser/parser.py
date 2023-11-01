import ctypes
from Parser.exceptions import InvalidSyntax
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
        self._file_path = file_path

    def run (self):
        self._load_file(self._file_path)

        while(self._asm_lines):
            self._parse_line()
        
        self._operation_lines.append(hex(self._current).lstrip("0x").upper())
        
        self._write_file('P4.o')

    def _parse_line (self):
        asm_line = self._asm_lines.pop(0).lstrip().split(' ')
        op_code = ''
        try:
            if (asm_line[0] == 'ORG'):
                self._current = stov(asm_line[1])
            else:
                monic = mnemonics.match(asm_line[0])
                
                if (monic is None):
                    asm_line = self._label(asm_line)

                if (asm_line):
                    monic = mnemonics.match(asm_line[0])
                    op_code = self._get_op_code(asm_line,monic)
                    self._operation_lines.append(f'{op_code}\n')


        except IndexError:
            raise InvalidSyntax('Missing arguments',self._current)
        
        except IndentationError or ValueError:
            raise InvalidSyntax('Invalid number',self._curent)

    def _get_op_code(self,asm_line,monic):
        if (monic is None):
            raise InvalidSyntax('Invalid instruction',self.current)
        op_code = ''
        
        if (len(asm_line) == 1 and monic.get('INH')):
            op_code = f'{hex(self._current).lstrip("0x").upper()} {monic["INH"]}'

            self._current += len(monic["INH"].split(' '))

        elif (asm_line[1].startswith('#') and monic.get('IMM')):
            op_code = self._parse_IMM(asm_line[1],monic['IMM'])
            op_code = f'{hex(self._current).lstrip("0x").upper()} {op_code}'

            self._current += len(monic["IMM"].split(' '))
        else:
            op_code,proto = self._parse_args(asm_line[1],monic)
            op_code = f'{hex(self._current).lstrip("0x").upper()} {op_code}'

            self._current += len(monic[proto].split(' '))

        
        return op_code
    
    def _parse_IMM (self,asm_line:str,proto:str):
        proto = proto.split(' ')
        op_code = proto.pop(0)
        asm_line = stov(asm_line[1:])

        if (len(proto) > 1):
            asm_line = format(asm_line,'04x').upper()
            asm_line = f'{asm_line[:2]} {asm_line[2:]}'
            op_code += f' {asm_line}'

        else:
            asm_line = format(asm_line,'02x').upper()
            op_code += f' {asm_line}'

        return op_code
    
    def _parse_args (self,asm_line:str,monic):
        op_code = ''
        try:
            asm_line, proto = self._get_addr_mode(asm_line,monic)
        except IndexError:
            raise InvalidSyntax('Missing arguments',self._current)
        
        if (proto == 'DIR'):
            asm_line = format(asm_line,'02x').upper()
            op_code = f'{monic[proto].split(" ")[0]} {asm_line}'

        elif (proto == 'EXT'):
            asm_line = format(asm_line,'04x').upper()
            asm_line = f'{asm_line[:2]} {asm_line[2:]}'
            op_code = f'{monic[proto].split(" ")[0]} {asm_line}'
        
        return op_code,proto
        


    def _get_addr_mode (self,asm_line:str,monic):
        if (asm_line.startswith(',')):
            pass
        
        else:
            asm_line = asm_line.split(',')
            
            if (len(asm_line) > 1):
                pass
            else:
                asm_line = stov(asm_line[0])
                if (asm_line > 255 and monic.get('EXT')):
                    return asm_line, 'EXT'
                
                elif (asm_line <= 255 and monic.get('DIR')):
                    return asm_line, 'DIR'
                
                else:
                    raise InvalidSyntax('Bas Address mode',self.current)

            


    def _label(self,asm_line):
        asm_line = asm_line[0].split('\t')
        try:
            if (asm_line[1] == 'EQU'):
                self._labels.append({asm_line[0]:int(stov(asm_line[2]))})
                asm_line.clear()

            elif (asm_line[1] == 'END'):
                self._labels.append({asm_line[0]:self._current})
                asm_line.clear()

            elif (mnemonics.match(asm_line[1]) is not None):
                self._labels.append({asm_line[0]:self._current})
                asm_line.pop(0)

            else:
                raise InvalidSyntax('Invalid arguments',self)

        except IndexError as err:
            raise InvalidSyntax('Missing arguments',self._current)
        
        except IndentationError or ValueError:
            raise InvalidSyntax('Invalid number',self._current)

        return asm_line


    def _load_file (self, path:str):
        with open(path,'r',encoding='utf-8') as file:
            self._code_str = file.read()

        self._asm_lines = self.code_str.splitlines()

    @property
    def code_str (self):
        return self._code_str


    def _write_file (self, path:str):
        with open(path,'w',encoding='utf-8') as file:
            file.writelines(self._operation_lines)
