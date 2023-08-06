from .CodeGen import *
from .Context import *

def run(directory='.', contexts=None, verbose=False):
    '''
    contexts should be [(extension, ctx class)]
    '''
    if not directory:
        directory = '.'
    if not directory.endswith("/"):
        directory += "/"
    if not contexts:
        contexts = [("", CodeGenCtx)]
    filepath = directory + '**'
    for filename in find_files(filepath):
        for ext, ctx in contexts:
            if not ext or filename.endswith("." + ext):
                CodeGen(filename, ctx, verbose).generate_code()
                break