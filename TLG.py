#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
"""
Ternary Landscape Generator Python Launcher

"""

import sys
import os
from copy import deepcopy
import pprint

# Python 2/3 support
PY3 = sys.version_info >= (3,)
PY2 = not PY3

class Parset:
	"""A set of map-generation parameters"""
	names = []
	def __init__(self, name, pars):
		self.names.append(name)
		self.pars = pars
	def __iter__(self):
		for attr in dir(Parset):
			if not attr.startswith("__"):
				yield attr
	pass

class Maplist:
		"""A list of maps"""
		pass


tmp = sys.argv[1]

file = os.path.basename(tmp)
path = os.path.split(tmp)[0]
pf	 = os.path.abspath(tmp)
print ('\nBasename:', file)

"""
		Reading input
"""
decs = {}	# decs is a "dictionary" object.
					# decs are declensions of maps (some pars are arrays)
current = None
f = open(pf, 'r')							# We open the file
mylines = f.read().splitlines()
f.close()											# We close the file
varlist = {}
for line in mylines:
	nm 	= line.split(":")[0]
	val = line.split(":")[1:]
	if nm == "#": continue 			# Comment, skipping line
	if len(val) < 1: 						# Check if empty line => save variables
		print("End of", current, "parameters, storing list...")
		decs[current] = Parset(current, varlist)
		current = None
		varlist = {}		# Otherwise later modifs will affect previous decs[]
		continue
	if current is None: 				# New parameter set => store name
		current = val[0]
		continue
	# Save parameter into dictionary
	varlist[nm] = val[:]
"""
We need to store the last declenson, otherwise it's lost
If there is no empty line followed by a comment in the parser file
"""
print("End of file, saving parameters for", current, "...")
decs[current] = Parset(current, varlist)

"""
		Filling in the gaps
"""

print("\n\n")
for x in decs:
	#~ print ("Declenson: ", x)
	if "REPLICATES" not in decs[x].pars:
		print("Assuming 1 replicate for dec", x)
		decs[x].pars["REPLICATES"] = [1]
	if "P2" not in decs[x].pars:
		print("P2 is missing")
		if "P0" in decs[x].pars:
			print("P0 is",	decs[x].pars["P0"])
			if  "P1" in decs[x].pars:
				print("P1 is",	decs[x].pars["P1"])
				# TODO: Not guessable if both attributes are array
				# TODO: Gues if one attribute is array
				#~ decs[x].pars["P2"] = list()
				#~ decs[x].pars["P2"] = 
				decs[x].pars["P2"] = [round(1 -
															float(decs[x].pars["P0"][0]) -
															float(decs[x].pars["P1"][0]), 4)]
				print("So P2 is",	decs[x].pars["P2"])
			else:
				raise NameError("You nead to define at least two of 'P0', 'P1' and 'P3'")
	#~ print (vars(decs[x]))

decnames = list(decs.keys())
print("done\n")
print(vars(decs["F50"]))

""" Creating the actual map sets """

def unroll (dec,						# declenson object
						maps=None,			# List of maps already created
						roll="",				# Depth marker
						checked=None,		# List of parameters unrolled
						recurs=False):	# Is the function being called by itself?
	""" Recursively unroll declenson object to create as many maps
			as there are possible combinations of parameters
	"""
	# Needed to fix design flaw of default pars
	if maps is None:
		maps = list()
	depth = 0

	def savemap (mymap, maps, roll):
		print(roll, " Saving map", len(maps)+1)
		maps.append(mymap.pars.copy())
	
	def checkpar (mymap, maps, par, parnames, roll, depth, skip=False):
		depth += 1
		par = parnames[depth-1]
		roll=roll+">"+par

		if len(mymap.pars[par]) > 1:
			""" Multiple values for parameter 'par' """
			values = mymap.pars[par]																					# Storing the values to restore them later
			print(roll, "= ", values)
			for x in values:
				#~ if x == values[-1]: print("Last value: SKIP!!!")
				print(roll, "=", x)
				localmap = deepcopy(mymap)																			# We work on a temporary copy of the parameter set
				localmap.pars[par] =  [x]																				# Now parameter 'par' has a single value
				#~ print(roll, "depth", depth, "/", len(parnames))
				if depth < (len(parnames)):
					""" We are NOT working on the last parameter """							# Usually the last is Y_SIZE, but keeps it flexible
					if not skip: skip = (x == values[-1])													# Check if we should skip saving
					""" x is NOT the last value of this parameter """
					res = checkpar(mymap=localmap, maps=maps, par=par,
													parnames=parnames, roll=roll, depth=depth,		# Recursity! Checking if there any multi-value params left
													skip=skip)
					maps 	= res['maps']																						# Updating values from the resukt of checkpar()
					mymap = res['mymap']
					skip 	= (x == values[-1])			# <<- probably useless					# We need to check again if we should skip next saving
					skip 	= res['skip']						# <<- Usefull										# But should be overriden by the result of res 
					#~ if skip: print("possible skip", mymap.pars["X_SIZE"])

					
					if (depth == (len(parnames) -1)) and len(mymap.pars[parnames[-1]]) == 1 :
						""" x is the last value of this par AND this par is the
								last of the dataset
						"""
						savemap(mymap, maps, roll)																	# We save the map
						skip = False																								# Next save should not be skipped (start from scratch)

						
				elif depth == (len(parnames)):
					""" The current param is the last one """
					savemap(localmap, maps, roll)																	# Save
					skip = True																										# Skip the next save (Already saved)
			print(roll, "<< restoring")
			mymap.pars[par] = values																					# Restoring the initial valueS of the parameter
		else:
			""" Only one value for this param """
			print(roll);
			if depth < len(mymap.pars):
				""" This is NOT the last parameter """
				res = checkpar(mymap=mymap, maps=maps, par=par,									# Need to check for the other parameters
												parnames=parnames, roll=roll, depth=depth)
				maps = res['maps']
				mymap = res['mymap']																						# Updating values from the resukt of checkpar()
				skip = res['skip']
			#~ print(roll, "depth", depth, "of", len(parnames))
			if (depth == (len(parnames) -1)) and not skip:
				""" This is the last parameter and
						the map has not been saved yet
				"""
				savemap(mymap, maps, roll)																			# Save
				skip=False																											# Next save should not be skipped (start from scratch)
			#~ print(roll, "\t", par, "= ", mymap.pars[par])
		return({'maps':maps, 'mymap':mymap, "skip":skip})										# End of the function, returning object as a dict
	#~ if recurs is False: print("Unrolling...")

	
	print(roll, "Checking for multiple values...")
	localmap	= None 																											# To prevent pesky ghost values
	mymap			= None
	values		= None
	mymap			= deepcopy(dec)																							# Prevent overwriting the original dec
	parnames = sorted(list(mymap.pars.keys()))														# To provide repeatability
	#~ print(parnames)

	if list(mymap.pars.keys())[0] == "NAME":
		""" First parameter ins "name", should have only one value """
		param = list(mymap.pars.keys())[0]																	# Not working on the first param
	else:
		param = list(mymap.pars.keys())[1]																	# Working on the (next) first param
	res = checkpar(mymap, maps, param, parnames=parnames,
									roll=roll, depth=depth);															# Roll is an indicator of where the function is working (for debug-ing)
	#~ print("alligator")
	maps = deepcopy(res['maps']);																					# Getting the results back
	mymap = res["mymap"];

	
	
	print(roll, "Leaving function with", len(maps), "maps")
	return({'maps':maps, 'mymap':mymap})


maps = {}


for dec in sorted(decnames):
	print("unrolling for", dec)
	declen = None
	res = None
	declen = decs[dec]
	res = unroll(declen)
	maps[dec] = res['maps']
	
#~ dec="F50"; res=None
#~ declen = decs[dec]
#~ res = unroll(declen)
#~ maps[dec] = res['maps']




#~ print("Final maps are")
#~ for x in sorted(maps):
	#~ print ("\n", len(maps[x]), "maps in", x)

#~ print("Final maps are")
#~ for x in sorted(maps):
	#~ print ("\ndec", x)
	#~ for m in maps[x]: print(" :Q11", m['Q11']," :Q22", m['Q22']," :X_SIZE", m['X_SIZE']," Y_SIZE", m['Y_SIZE']," :P1", m['P1'])

print("Final maps are")
for x in sorted(maps):
	for m in maps[x]:
		tmp = {k: m[k] for k in ("P0", "P1", "X_SIZE", 'Q11', 'Q22')}
		pprint.pprint(tmp, width=4)



mapnames = list(maps.keys())

#
# Printing the maps into .in files
#
# A dedicated function:
#
def map2in( mapdict, mapname, mapid=None, suffix=".in"):
	"This prints a passed string to a passed file"
	mymap = mapdict
	name = mapname
	if mapid is not None:
		""" There is a map replicate ID, should add it to the name """
		name = name + "_" +str(mapid).zfill(4)														# 4 digits -> up to 9999 maps
	# Opening file
	filename = name + suffix
	file = open(filename, "w")
	# Writing content
	file.write("[NAME:"+ name +"] => Name of the generated landscape\n")
	file.write("[X_SIZE:" + str(int(float(mymap["X_SIZE"][0]))) + "]X[Y_SIZE:" + str(int(float(mymap["Y_SIZE"][0]))) + "] => size of the landscape\n")
	file.write("[P1:" + str(float(mymap["P1"][0])) + "] => proportion of type 1 (agricultural)\n")
	file.write("[P2:" + str(float(mymap["P2"][0])) + "] => proportion of type 2 (urban)\n")
	file.write("[Q11:" + str(float(mymap["Q11"][0])) + "] => P(11|1*)\n")
	file.write("[Q11:"+ str(float(mymap["Q22"][0])) + "] => P(22|2*)\n")
	file.write("[MAX_ITERATIONS:" + str(int(float(mymap["MAX_ITERATIONS"][0]))) + "] => Max number of iterations\n")
	file.write("[ERROR_THRESHOLD:"+ str(int(float(mymap["ERROR_THRESHOLD"][0]))) + "] => Min value of delta to keep going\n")
	file.write("[METHOD:"+ mymap["METHOD"][0] + "] => Method to compute delta\n")
	file.write("[SEED:"+ str(int(float(mymap["SEED"][0]))) + "] => Random seed number, set to 0 for random\n")
	# Closing file
	file.close()
	return;

#
# Looping over all maps
#
print("\n")

for x in sorted(maps):
	i = 0
	for m in maps[x]:
		i += 1
		reps = list(range(int(m["REPLICATES"][0])))													# Create a list 0:REPLICATES
		reps = [x+1 for x in reps] 																					# add 1 to reps : 1:(REPLICATES +1)
		print("Creating '.in' file(s) for map",
						str(i).zfill(3), "declension " + x,
						"(", m["REPLICATES"][0], "replicates)")
		for r in reps :
			# TODO: Implement offset for replicates (in case we want additional maps
			map2in(mapdict=m, mapname=x+"_"+str(i).zfill(3), mapid=r)
