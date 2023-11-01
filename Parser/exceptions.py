class InvalidSyntax (Exception):
    def __init__(self,msg,line):
        self.message = f"Invalid syntax in asm line [{hex(line).lstrip('0x').upper()}] Error message: [{msg}]"
        super().__init__(self.message)