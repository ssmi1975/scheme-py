def translate(text, debug=False):
    from .parser import parse
    from .translator import translate
    return translate(parse(text, debug=debug))

def execute(text, debug=False):
    from .model import Context
    from .executor import execute
    from .stdproc import BINDINGS
    return execute(translate(text, debug=False), Context(BINDINGS))
