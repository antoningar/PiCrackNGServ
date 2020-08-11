#!/usr/bin/env python

import json

def dumpListObject(listObject):
    return json.dumps([o.__dict__ for o in listObject], indent=4)

def dumpObject(o):
    return json.dumps(o.__dict__,indent=4)

def loadObject(network):
    return json.loads(network)