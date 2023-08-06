from .magics import NbDiffMatchPatchMagic

__version__="0.0.1"

def load_ipython_extension(ipython):
    ipython.register_magics(NbDiffMatchPatchMagic)
