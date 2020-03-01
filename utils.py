def is_name_start(x: str):
    return x.isalpha() or x == '_'

def is_name_char(x: str):
    return x.isalpha() or x.isnumeric() or x == '-' or x == ':'

def is_whitespace(x: str):
    return x in ' \t\n'