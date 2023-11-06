from ctypes import c_int16,c_uint16,c_int8,c_uint8
from Parser.exceptions import InvalidSyntax
from Utilities import error_codes as e_cds
from Utilities.casting import stov
from Utilities import files
from Utilities import mnemonics

class Parser:
    def __init__ (self,file_path,write_path):
        self._asm_lines = []
        self._code_str = ''
        self._current = ''
        self._tabsim = []
        self._operation_lines = []
        self._pending = []
        self._file_path = file_path
        self.write_path = write_path

    def run (self):
        self._load_file(self._file_path)

        while(self._asm_lines):
            if self._parse_line():
                break

        self._asm_lines = self.code_str.splitlines()
        self._operation_lines.clear()

        while(self._asm_lines):
            if self._parse_line():
                break
        
        self._write_file(self.write_path)

    def _parse_line (self):
        asm_line = self._asm_lines.pop(0).lstrip().split(' ')
        if '\t' in asm_line[0]:
            label = asm_line[0].split('\t')
            asm_line[0] = label[1]
            asm_line.insert(0,label[0])
        op_code = ''
        is_end = False
        try:
                asm_line = self._label(asm_line)

                if (asm_line):
                    asm_line,is_end = self._parse_directive(asm_line,is_end)

                if (asm_line):
                    if (self._current != ''):
                        monic = mnemonics.m_match(asm_line[0])
                        op_code = self._get_op_code(asm_line,monic)
                    else:
                        raise InvalidSyntax('Must define line address first',-1)
                    self._operation_lines.append(f'{op_code}\n')

        except IndexError:
            raise InvalidSyntax('Missing arguments',self._current)

        except IndentationError or ValueError:
            raise InvalidSyntax('Invalid number',self._curent)

        return is_end

    def _get_op_code(self,asm_line,monic):
        if (monic is None):
            raise InvalidSyntax('Invalid instruction',self.current)
        op_code = ''

        if (len(asm_line) == 1 and monic.get('INH')):
            op_code = f'{format(self._current,"04x").upper()} {monic["INH"]}'

            self._current += len(monic["INH"].split(' '))

        elif (asm_line[1].startswith('#') and monic.get('IMM')):
            op_code = self._parse_IMM(asm_line[1],monic['IMM'])
            op_code = f'{format(self._current,"04x").upper()} {op_code}'

            self._current += len(monic["IMM"].split(' '))
        else:
            op_code,proto = self._parse_args(asm_line[1],monic)
            op_str = op_code
            op_code = f'{format(self._current,"04x").upper()} {op_code}'

            if op_str == 'NOP':
                self._current += len(monic[proto].split(' '))
            else:
                self._current += len(op_str.split(' '))


        return op_code

    def _parse_directive (self,asm_line:list[str],is_end: bool,is_pending=False):
        monic = mnemonics.d_match(asm_line[0])
        if (monic is not None):
            try:
                asm_line.pop(0)
                if monic == 0:
                    self._current = 0
                elif monic == 1:
                    self._current = stov(asm_line.pop(0),self._tabsim)
                elif (self._current != ''):
                    if monic == 2:
                        self._operation_lines.append(f'{format(self._current,"04x").upper()}')
                        is_end = True
                    elif monic == 3:
                        data_str = ''
                        data = []
                        if (asm_line):
                            data = asm_line.pop(0).split(',')

                            for item in data:
                                if item.startswith("'"):
                                    u_comma = "'"
                                    data_str = f'{data_str} {format(ord(item.lstrip(u_comma)),"02x").upper()}'
                                else:
                                    data_str = f'{data_str} {format(stov(item,self._tabsim),"02x").upper()}'
                        else:
                            data_str = ' 00'
                            data.append(data_str)

                        self._operation_lines.append(f'{format(self._current,"04x").upper()}{data_str}\n')
                        self._current = self._current + len(data)
                    elif monic == 4:
                        data_str = ''
                        data = []
                        if (asm_line):
                            data = asm_line.pop(0).split(',')
                            for item in data:
                                if item.startswith("'"):
                                    u_comma = "'"
                                    item_str = format(ord(item.lstrip(u_comma)),"04x").upper()
                                    item_str = f'{item_str[:2]} {item_str[2:]}'
                                    data_str = f'{data_str} {item_str}'
                                else:
                                    item_str = format(stov(item,self._tabsim),"04x").upper()
                                    item_str = f'{item_str[:2]} {item_str[2:]}'
                                    data_str = f'{data_str} {item_str}'
                        else:
                            data_str = ' 00 00'
                            data.append(data_str)

                        self._operation_lines.append(f'{format(self._current,"04x").upper()}{data_str}\n')
                        self._current = self._current + (len(data)*2)
                    elif monic == 5 or monic == 6:
                        data = int(asm_line.pop(0))
                        data_str = ''
                        for i in range(data):
                            data_str = data_str + ' 00'
                        self._operation_lines.append(f'{format(self._current,"04x").upper()}{data_str}\n')
                        self._current = self._current + data
                    elif monic == 7:
                        data_str = ''
                        data = []
                        if (asm_line):
                            data = asm_line.pop(0).split(',')

                            for item in data:
                                data_str = f'{data_str} {format(stov(item,self._tabsim),"02x").upper()}'
                        else:
                            data_str = ' 00'
                            data.append(data_str)

                        self._operation_lines.append(f'{format(self._current,"04x").upper()}{data_str}\n')
                        self._current = self._current + len(data)
                    elif monic == 8:
                        cons_str = [x for x in asm_line.pop(0).strip('/')]
                        data_str = ''
                        for char in cons_str:
                            char = format(ord(char),'02x').upper()
                            data_str = f'{data_str} {char}'
                        self._operation_lines.append(f'{format(self._current,"04x").upper()}{data_str}\n')
                        self._current = self._current + len(cons_str)
                    elif monic == 9:
                        data,length = asm_line.pop(0).split(',')
                        length = int(length)
                        data = int(data)
                        data_str = ''
                        for i in range (length):
                            data_str = data_str + f' {format(data,"02x").upper()}'
                        self._operation_lines.append(f'{format(self._current,"04x").upper()}{data_str}\n')
                        self._current = self._current + length
                else:
                    raise InvalidSyntax('Must define line address first',-1)
            except IndexError:
                raise InvalidSyntax('Missing arguments',self._current)
            except ValueError:
                raise InvalidSyntax("Invalid Addres Number",self._current)
        return asm_line,is_end





    def _parse_IMM (self,asm_line:str,proto:str):
        proto_list = proto.split(' ')
        op_code = proto_list.pop(0)
        asm_line = stov(asm_line[1:],self._tabsim)

        if asm_line is not None:
            if (len(proto_list) > 1):
                asm_line = format(asm_line,'04x').upper()
                asm_line = f'{asm_line[:2]} {asm_line[2:]}'
                op_code += f' {asm_line}'

            else:
                asm_line = format(asm_line,'02x').upper()
                op_code += f' {asm_line}'
        else:
            op_code = proto
            self

        return op_code

    def _parse_args (self,asm_line:str,monic):
        op_code = ''
        try:
            asm_line, proto = self._get_addr_mode(asm_line,monic)
        except IndexError:
            raise InvalidSyntax('Missing arguments',self._current)
        
        if asm_line is None:
            self._pending.append(len(self._operation_lines))
            op_code = monic[proto]
        else:
            if (proto == 'DIR'):
                asm_line = format(asm_line,'02x').upper()
                op_code = f'{monic[proto].split(" ")[0]} {asm_line}'

            elif (proto == 'EXT'):
                asm_line = format(asm_line,'04x').upper()
                asm_line = f'{asm_line[:2]} {asm_line[2:]}'
                op_code = f'{monic[proto].split(" ")[0]} {asm_line}'

            elif (proto == 'IDX'):
                number, xysp = asm_line
                number = stov(number,[]) if not number == '' else 0
                
                xysp = mnemonics.get_xysp(xysp)
                if (number in range (16)):
                    p_bin = 'rr0nnnnn'
                    number = format(number,'05b')
                    p_bin = p_bin.replace('rr',xysp)
                    p_bin = p_bin.replace('nnnnn',number)
                    p_bin = format(int(p_bin,2),'02x').upper()
                    op_code = f'{monic[proto]} {p_bin}'
                elif (number in range(-16,1)):
                    p_bin = 'rr0nnnnn'
                    number = c_uint8 (number).value
                    number = format(number,'08b')
                    number = number[-5:]
                    p_bin = p_bin.replace('rr',xysp)
                    p_bin = p_bin.replace('nnnnn',number)
                    number = format(int(number,2),'02x').upper()
                    p_bin = format(int(p_bin,2),'02x').upper()
                    op_code = f'{monic[proto]} {p_bin}'
                else:
                    p_bin = '111rr0zs'.replace('rr',xysp)
                    if (number in range (-256,256)):
                        p_bin = p_bin.replace('z','0')
                        if (number < 0):
                            p_bin = p_bin.replace('s','1')
                        else:
                            p_bin = p_bin.replace('s','0')
                        number = format(c_uint8(number).value,'02x').upper()
                        op_code = f'{monic[proto]} {format(int(p_bin,2),"02x").upper()} {number}'
                    else:
                        p_bin = p_bin.replace('z','0')
                        if (number < 0):
                            p_bin = p_bin.replace('s','1')
                        else:
                            p_bin = p_bin.replace('s','0')
                        number = format(c_uint16(number).value,'04x').upper()
                        op_code = f'{monic[proto]} {format(int(p_bin,2),"02x").upper()} {number[:2]} {number[2:]}'

            elif (proto == 'REL'):
                rel = monic['REL'].split(' ')
                if (len(rel) > 2):
                    result = c_uint16(asm_line-(self._current+len(rel))).value
                    rstr = format(result,'04x').upper()
                    op_code = f'{rel[0]} {rel[1]} {rstr[:2]} {rstr[2:]}'
                else:
                    result = c_int16 (asm_line-(self._current+len(rel))).value
                    u_result = c_uint8 (asm_line-(self._current+len(rel))).value
                    if (result < 0 and u_result in range(0x80,0x100)):
                        rstr = format(u_result,'02x').upper()
                        op_code = f'{rel[0]} {rstr}'
                    elif (not (result < 0) and u_result in range(0x00,0x80)):
                        rstr = format(u_result,'02x').upper()
                        op_code = f'{rel[0]} {rstr}'
                    else:
                        op_code = 'NOP'
        return op_code,proto



    def _get_addr_mode (self,asm_line,monic):
        asm_line = asm_line.split(',')
        
        if (len(asm_line) > 1):
            return asm_line, 'IDX'
        else:
            asm_line = stov(asm_line[0],self._tabsim)
            if asm_line is None:
                return asm_line,'REL'
            
            elif (asm_line > 255 and monic.get('EXT')):
                return asm_line, 'EXT'

            elif (asm_line <= 255 and monic.get('DIR')):
                return asm_line, 'DIR'
            elif (monic.get('REL')):
                return asm_line, 'REL'
            else:
                raise InvalidSyntax('Bas Address mode',self.current)




    def _label(self,asm_line:list[str]):
        if mnemonics.m_match(asm_line[0]) is None and mnemonics.d_match(asm_line[0]) is None:
            label = asm_line.pop(0)
            is_in = False
            for item in self._tabsim:
                if (item.get(label)):
                    is_in = True
            try:
                if asm_line[0] == 'EQU':
                    equ_d = {label:stov(asm_line[1],self._tabsim)}
                    if not is_in:
                        self._tabsim.append(equ_d)
                    asm_line.clear()
                elif (self._current != ''):
                    if not is_in:
                        self._tabsim.append({label:self._current})
                else:
                    raise InvalidSyntax('Must define line address first',-1)
            except IndexError:
                raise InvalidSyntax('Missing arguments',self._current)
            except ValueError:
                raise InvalidSyntax("Invalid Addres Number",self._current)
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
            for i in self._operation_lines:
                file.write(i)
