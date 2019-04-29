def translate(text):
    from .parser import parse
    from .translator import translate
    return translate(parse(text))

def execute(text):
    from .executor import execute
    return execute(translate(text), {})
