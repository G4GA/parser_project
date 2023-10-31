import Utilities.error_codes as cds

def stov (return_code,value:str):
    return_value = 0
    if return_code == 0:
        try:
            if value.startswith('$'):
                return_value = int(value.lstrip('$'),16)
            elif value.startswith('@'):
                return_value = int(value.lstrip('@'),8)
            elif value.startswith('%'):
                return_value = int(value.lstrip('%'),2)
            else:
                return_value = int(value)
        except IndentationError or ValueError:
            print('Invalid number system')
            return_code = cds.INVALID_NUMBER_SYSTEM

    return (return_code,return_value)