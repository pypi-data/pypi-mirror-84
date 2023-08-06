from asthook.static.ast import Node, ast
import asthook.log

import javalang

from ..Taint import taint

class traversal:
    def __init__(self, name, type):
        self.name = name
        self.type = type

@Node("ClassCreator", "in")
class MethodDeclarationIn:

    @classmethod
    def call(cls, r, self):
        #log.debug(r)
        if self.elt.type.name == "FileOutputStream":
            r["traversal"] = True
        return r

@Node("ClassCreator", "out")
class MethodDeclarationOut:

    @classmethod
    def call(cls, r, self):
        r["traversal"] = False
        return r

@Node("MemberReference", "in")
class MemberReferenceIn:

    @classmethod
    def call(cls, r, self):
        if "traversal" in r and r["traversal"]:
            #log.debug(self.elt.member)
            #log.debug(taint.revxref(self.elt))
            #log.debug(taint.TaintElt.get([], self.elt.member))
            queue = [taint.TaintElt.get([], self.elt.member)]
            while len(queue) > 0:
                elt = queue.pop()
                for ep in elt.parent_get():
                    queue.append(ep)
                if type(elt.node_get()) == ast.LocalVariableDeclaration:
                    #log.debug(elt.node_get().elt.declarators[0].initializer.type.name)
                    if elt.node_get().elt.declarators[0].initializer.type.name == "EditText":
                        log.debug(f"Path traversal found at {elt.position()}"
                        f"with impact at {self.elt._position}")
        return r
