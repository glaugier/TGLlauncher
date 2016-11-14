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
pf	 = os.path.abspath(tmp)
print ('\nBasename:', file)

""" Reading input """
maps = {}	# map is a "dictionary" object.
current = None
f = open(pf, 'r')		 # We open the file
mylines = f.read().splitlines()
f.close()							 # We close the file
for line in mylines:
		nm = line.split(":")[0]
		val = line.split(":")[1:]
#		print("Arg", nm, "is", val)
		if len(val) < 1:
				current = None
				print("skipping blanck line")
				continue
		if current is None:
				current = val[0]
				maps[current] = Parset()

#		print("Saving in ", current)		
		setattr(maps[current], nm, val)

""" Filling in the gaps"""
		
print("\n\n")
for x in maps:
		print ("Map: ", x)
		if not hasattr(maps[x], "REPLICATES"):
				maps[x].REPLICATES = [1]
		if not hasattr(maps[x], "P2"):
				if hasattr(maps[x], "P0"):
						if hasattr(maps[x], "P1"):
								print("P0 is",	maps[x].P0[0])
								# TODO: Not guessable if both attributes are array
								# TODO: Gues if one attribute is array
								maps[x].P2 = 1 - float(maps[x].P0[0]) - float(maps[x].P1[0])
						else:
								raise NameError("You nead to define at least two of 'P0', 'P1' and 'P3'")
		print (vars(maps[x]))

print("\n\n first map:\n")

mapnames = list(maps.keys())

#
# Printing the maps into .in files
#
# A dedicated function:
#
def map2in( mapdict, mapname, mapid=None, suffix=".in"):
	"This prints a passed string to a passed file"
	mymap = mapdict[mapname]
	name = mymap.NAME[0]
	if mapid is not None:
			name = name + "_" +str(mapid).zfill(3)
	# Opening file
	filename = name + suffix
	file = open(filename, "w")
	# Writing content
	#~ file.write(vars(maps[x]))
	#~ text = ''.join(tuple)
	file.write("[NAME:"+ name +"] => Name of the generated landscape\n")
	file.write("[X_SIZE:" + str(int(float(mymap.X_SIZE[0]))) + "]X[Y_SIZE:" + str(int(float(mymap.Y_SIZE[0]))) + "] => size of the landscape\n")
	file.write("[P1:" + str(float(mymap.P1[0])) + "] => proportion of type 1 (agricultural)\n")
	file.write("[P2:" + str(round(float(mymap.P2), 2)) + "] => proportion of type 2 (urban)\n")
	file.write("[Q11:" + str(round(float(mymap.Q11[0]), 2)) + "] => P(11|1*)\n")
	file.write("[Q11:"+ str(round(float(mymap.Q22[0]), 2)) + "] => P(22|2*)\n")
	file.write("[MAX_ITERATIONS:" + str(int(float(mymap.MAX_ITERATIONS[0]))) + "] => Max number of iterations\n")
	file.write("[ERROR_THRESHOLD:"+ str(int(float(mymap.ERROR_THRESHOLD[0]))) + "] => Min value of delta to keep going\n")
	file.write("[METHOD:"+ mymap.METHOD[0] + "] => Method to compute delta\n")
	file.write("[SEED:"+ str(int(float(mymap.SEED[0]))) + "] => Random seed number, set to 0 for random\n")
	# Closing file
	file.close()
	return;
#
# Looping over all maps
#
print("\n")
for mapname in mapnames :
	print("Creating '.in' file(s) for map " + mapname)
	reps = list(range(int(maps[mapname].REPLICATES[0])))
	reps = [x+1 for x in reps] # add 1 to reps
	for i in reps :
		# TODO: Loop over replicates
		map2in(mapdict=maps, mapname=mapname, mapid=i)
