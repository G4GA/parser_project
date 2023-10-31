import Utilities.error_codes as cds

def stov (return_code,value:str):
    return_value = 0
    if return_code == 0:
            if value.startswith('$'):
                return_value = int(value.lstrip('$'),16)
            elif value.startswith('@'):
                return_value = int(value.lstrip('@'),8)
            elif value.startswith('%'):
                return_value = int(value.lstrip('%'),2)
            else:
                return_value = int(value)

    return (return_code,return_value)