
from asthook.static.module.register import ModuleStaticCmd

@ModuleStaticCmd("PathTraversal", "For the demo", bool)
class Tree:
    """
    Class Exemple of cresation static module
    """
    def __init__(self, package, tmp_dir, args):
        from . import pathtraversal
        return None

