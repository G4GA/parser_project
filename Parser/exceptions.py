class InvalidSyntax (Exception):
    def __init__(self,msg,line):
        self.message = f"Invalid syntax in asm line [{line}] Error message: [{msg}]"
        super.__init__(self.message)