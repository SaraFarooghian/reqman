#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import json


class HeadersMixedCase(dict):
    def __init__(self, **kargs):
        dict.__init__(self, **kargs)

    def __getitem__(self, key):
        d = {k.lower(): v for k, v in self.items()}
        return d.get(key.lower(), None)

    def get(self, key, default=None):
        d = {k.lower(): v for k, v in self.items()}
        return d.get(key.lower(), default)


def jdumps(o, *a, **k):
    k["ensure_ascii"] = False
    # ~ k["default"]=serialize
    return json.dumps(o, *a, **k)

def strjs(x) -> str:
    if type(x) is bytes:
        return str(x)
    elif type(x) is str:
        return x
    else:
        return jdumps(x)

class Test(int):
    """ a boolean with a name """

    name = ""

    def __init__(self, v, n1, n2, realValue):
        pass  # just for mypy

    def __new__(
        cls, value: int, nameOK: str = None, nameKO: str = None, realValue=None
    ):
        s = super().__new__(cls, value)
        if value:
            s.name = nameOK
        else:
            s.name = nameKO
        s.value = realValue
        return s

    def __repr__(self):
        return "%s: %s" % ("OK" if self else "KO", self.name)


def guessValue(txt):
    if type(txt) == str:
        try:
            return json.loads(txt)
        except:
            try:
                return json.loads('"%s"' % txt.replace('"', '\\"'))
            except:
                return txt
    return txt


def getValOpe(v):
    if type(v) == str and v.startswith("."):
        g = re.match(r"^\. *([\?!=<>]{1,2}) *(.+)$", v)
        if g:
            op, v = g.groups()
            if op in ["==", "="]:  # not needed really, but just for compatibility
                return v, lambda a, b: b == a, "=", "!="
            elif op == "!=":
                return v, lambda a, b: b != a, "!=", "="
            elif op == ">=":
                return (
                    v,
                    lambda a, b: b != None and a != None and b >= a or False,
                    ">=",
                    "<",
                )
            elif op == "<=":
                return (
                    v,
                    lambda a, b: b != None and a != None and b <= a or False,
                    "<=",
                    ">",
                )
            elif op == ">":
                return (
                    v,
                    lambda a, b: b != None and a != None and b > a or False,
                    ">",
                    "<=",
                )
            elif op == "<":
                return (
                    v,
                    lambda a, b: b != None and a != None and b < a or False,
                    "<",
                    ">=",
                )
            elif op == "?":
                return (
                    v,
                    lambda a, b: str(a) in str(b),
                    "contains",
                    "doesn't contain",
                )
            elif op in ["!?",]:
                return (
                    v,
                    lambda a, b: str(a) not in str(b),
                    "doesn't contain",
                    "contains",
                )
    return v, lambda a, b: a == b, "=", "!="

def testCompare(var: str, val, opeval) -> Test:
    value,fct,tok,tko=getValOpe(opeval)
    value=guessValue(value)

    test=fct(value,guessValue(val))

    nameOK = var + " " + tok + " " + strjs(value)  # test name OK
    nameKO = var + " " + tko + " " + strjs(value)  # test name KO
    return Test( test ,nameOK, nameKO,val )

if __name__=="__main__":
    pass
