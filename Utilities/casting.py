import Utilities.error_codes as cds

def stov (value:str,labels:list[str]):
    return_value = None
    try:
        if value.startswith('$'):
            return_value = int(value.lstrip('$'),16)
        elif value.startswith('@'):
            return_value = int(value.lstrip('@'),8)
        elif value.startswith('%'):
            return_value = int(value.lstrip('%'),2)
        else:
            return_value = int(value)
    except ValueError:
        for label in labels:
            if label.get(value):
                return_value = label[value]

    return return_value