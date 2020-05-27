#!/usr/bin/env python
"""
 flatten.py

 Intent:
      - Take a dictionary with Targets, and a list of dependencies
          and flatten to determine the proper build order

 Jake Prickett - May 2020
"""

from types import ListType

def _order(idepdict, val=None, level=0):
    results = {}
    if val is None:
        for k, v in idepdict.items():
            for dep in v:
                results.setdefault(k, 0)
                d = _order(idepdict, val=dep, level=level+1)
                for dk, dv in d.items():
                    if dv > results.get(dk, 0):
                        results[dk] = dv
        return results
    else:
        results[val] = level
        deps = idepdict.get(val, None)
        if deps is None or deps == []:
            return {val: level}
        else:
            for dep in deps:
                d = _order(idepdict, val=dep, level=level+1)
                for dk, dv in d.items():
                    if dv > results.get(dk, 0):
                        results[dk] = dv
            return results

def _invert(d):
    i = {}
    for k, v in d.items():
        if isinstance(v, ListType):
            for dep in v:
                depl = i.get(dep, [])
                depl.append(k)
                i[dep] = depl
        else:
            depl = i.get(v, [])
            depl.append(k)
            i[v] = depl
    return i

def flatten(depdict):
    #Generate an inverted deplist
    ideps = _invert(depdict)

    #generate relative order
    order = _order(ideps)

    #Invert the order
    iorder = _invert(order)

    #Sort the keys and append to a list
    output = []
    for key in sorted(iorder.iterkeys()):
        output.extend(iorder[key])
    return output
