
from asthook.static.module.register import ModuleStaticCmd
from asthook.utils import Output

@ModuleStaticCmd("vuln_data", "found vuln intent deeplink", str)
class Tree:
    """
    Class VulnData to found vulnerable intent used putData like deeplink
    "normal" for nopoc
    "poc" for poc
    """
    def __init__(self, package, tmp_dir, args):
        if not "exported" in Output.get_store()["manifest"]["activity"]:
            return
        from ..name_file import name_file_node
        from . import vuln_intent
        if args.vuln_intent == "poc":
            vuln_intent.poc = True

