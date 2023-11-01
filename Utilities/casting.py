import Utilities.error_codes as cds

def stov (value:str):
    return_value = 0
    if value.startswith('$'):
        return_value = int(value.lstrip('$'),16)
    elif value.startswith('@'):
        return_value = int(value.lstrip('@'),8)
    elif value.startswith('%'):
        return_value = int(value.lstrip('%'),2)
    else:
        return_value = int(value)

    return return_value