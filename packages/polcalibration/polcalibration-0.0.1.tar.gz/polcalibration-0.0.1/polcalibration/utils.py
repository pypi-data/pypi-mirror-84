import numpy as np
from __casac__.table import table as tb

def degreesToRadians(degrees):
    return degrees * np.pi / 180.0

def radiansToDegrees(radians):
    return radians * 180.0 / np.pi

def queryTable(query=""):
    return tb.taql(query+" AS "+tablename)
