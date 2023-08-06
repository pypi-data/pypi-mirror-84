from asthook.static.ast import Node
from asthook.utils import Output
from asthook.log import debug
from asthook.api_key_detector import detector



@Node("Literal", "in")
class ClassDeclarationIn:
    @classmethod
    def call(cls, r, self):
        if len(self.elt.value) > 0 and self.elt.value[0] == '"' and \
                self.elt.value[-1] == '"':
                    try:
                        if detector.detect_api_keys([self.elt.value[1:-1]])[0]:
                            debug(f"{self.elt.value} {r['Filename']}:{self.elt._position}")
                    except:
                        pass
        return r

