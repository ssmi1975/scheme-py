from .translator import translate

def translate(text):
    from .parser import parse
    from .translator import translate
    return translate(parse(text))

