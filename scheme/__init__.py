from .execute import execute

def execute(text):
    from .parser import parse
    from .execute import execute
    return execute(parse(text))

