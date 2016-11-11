#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
"""
Ternary Landscape Generator Python Launcher

"""



import sys
import os

# Python 2/3 support
PY3 = sys.version_info >= (3,)
PY2 = not PY3

class Parset:
    """A set of map-generation parameters"""
    pass
class Maplist:
    """A list of maps"""
    pass

tmp = sys.argv[1]

file = os.path.basename(tmp)
path = os.path.split(tmp)[0]
pf   = os.path.abspath(tmp)
print ('\nBasename:', file)

""" Reading input """
maps = {}
current = None
f = open(pf, 'r')     # We open the file
mylines = f.read().splitlines()
f.close()               # We close the file
for line in mylines:
    nm = line.split(":")[0]
    val = line.split(":")[1:]
#    print("Arg", nm, "is", val)
    if len(val) < 1:
        current = None
        print("skipping blanck line")
        continue
    if current is None:
        current = val[0]
        maps[current] = Parset()

#    print("Saving in ", current)    
    setattr(maps[current], nm, val)

""" Filling in the gaps"""
    
print("\n\n")
for x in maps:
    print ("Map: ", x)
    if not hasattr(maps[x], "P2"):
        if hasattr(maps[x], "P0"):
            if hasattr(maps[x], "P1"):
                print("P0 is",  maps[x].P0[0])
                # TODO: Not guessable if both attributes are array
                # TODO: Gues if one attribute is array
                maps[x].P2 = 1 - float(maps[x].P0[0]) - float(maps[x].P1[0])
            else:
                raise NameError("You nead to define at least two of 'P0', 'P1' and 'P3'")
    print (vars(maps[x]))

#
# Printing to a file:
#
def printin( filename, string ):
	"This prints a passed string to a passed file"
	# Opening file
	file = open(filename, "w")
	# Writing content
	#~ file.write(vars(maps[x]))
	file.write(string)
	# Closing file
	file.close()
	return;

printin(filename="test.in", string="Printed")
