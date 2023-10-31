def load_file (path:str):
    code = ''
    with open(path,'r',encoding='utf-8') as file:
        code = file.read()
    return code


def write_file (path:str,object_code):
    with open(path,'w',encoding='utf-8') as file:
        file.write(object_code)
