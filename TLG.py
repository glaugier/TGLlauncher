#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
"""
Ternary Landscape Generator Python Launcher

"""

import sys
import os
from copy import deepcopy
import pprint
import subprocess
import multiprocessing
import threading
from queue import Queue
import time

import argparse

"""
First we need to parse the command line arguments.
"""

parser = argparse.ArgumentParser(prog="tlg-launcher",
				description='Processes parset files into all combitations of parameters, generates .in files and launches tlg-core')
parser.add_argument('--version', action='version', version='%(prog)s 0.12.1')
parser.add_argument('parsets', type=str, nargs='+',
										help='The parset files to be parsed')
parser.add_argument('--dry', action='store_true', default=False,
										help='Creates .in files but does not launch tlg-core')
parser.add_argument('--verbose', '-V', action='store_true', default=False,
										help='Creates .in files but does not launch tlg-core')

args = parser.parse_args()
parsets = args.parsets																									# A list of parsets
dry     = args.dry																											# Dry run (no launching tlg-core)
verb    = args.verbose																									# Verbose mode
if dry and verb : print("Dryn-run mode: will not launch tlg")

"""
We've imported threading, queue and time. Threading is for, threading,
queue is going to help us make, you guessed it, a queue! Finally,
we import time. Our only reason for importing time here is to simulate
some idle time with a time.sleep() function.

Next, we're going to define a thread lock. The idea of a threading lock
is to prevent simultaneous modification of a variable.
So, if two processes begin interaction with a variable with it is, say,
5, and one operation adds 2, and the other adds 3, we're going to end
with either 7 or 8 as the variable, rather than having it be 5+2+3,
which would be 10. A lock will force an operation to wait until the
variable is unlocked in order to access and modify it. Another use for
a lock is to aid in input/output. With threading, it becomes quite easy
to have two processes modifying the same file, and the data will
literally just run over each other. So say you are meaning to save two
values, like "Monday" and "Tuesday" to a file, you are intending for
the file to just read: "Monday Tuesday," but instead it winds up looking
like "MoTunedsadyay." A lock helps this.

In this particular script, this is not actually useful, but still
good practice when multitheading.
"""

print_lock = threading.Lock()																						# A lock for printing

"""
Here, we're looking to use the lock to stop print functions from running
over each other in their output.

Now we're ready to create some sort of task to show off threading with:
"""

# The threader thread pulls an worker from the queue and processes it
def threader():
	" Creates Threads for workers to populate "
	while True:						# (No idea why)
		worker = q.get()																										# Gets an worker from the queue
		launchJob(worker)																										# Run the job with the avail worker in queue (thread)
		q.task_done()																												# Completed with the job

"""
Now we've used this "q," but we've not defined it, so we had better do
that:
"""
q = Queue()																															# Create the queue and threader 

"""
Now let's create our threads, and put them to work!
"""

# How many threads are we going to allow for?
ncpu = multiprocessing.cpu_count()																			# Getting the number of CPUs

for x in range(ncpu-1):																									# Launching one less to avoid saturation
	""" No more thant this number of CPUs """
	t = threading.Thread(target=threader)
	t.daemon = True																												# Classifying as a daemon, so they will die when the main dies
	t.start()																															# Begins, must come after daemon definition


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


decs = {}																																# decs is a "dictionary" object.
																																				# decs are declensions of maps (some pars are arrays)

"""
Now we need to do the following for each parameter set file in parsets
"""
for parset in parsets:
	thefile = os.path.basename(parset)
	path = os.path.split(parset)[0]
	pf	 = os.path.abspath(parset)

	""" In case of manual debugging
	file = "parset.txt"
	path = "./"
	pf= "./parset.txt"
	"""


	if verb : print ('\nBasename:', thefile)

	"""
			Reading input
	"""

	current = None
	f = open(pf, 'r')																											# We open the file
	mylines = f.read().splitlines()
	f.close()																															# We close the file
	varlist = {}
	for line in mylines:
		nm 	= line.split(":")[0]
		val = line.split(":")[1:]
		if nm == "#": continue 																							# Comment, skipping line
		if len(val) < 1: 																										# Check if empty line => save variables
			if verb: print("End of", current, "parameters, storing list...")
			decs[current] = Parset(current, varlist)
			current = None
			varlist = {}																											# Otherwise later modifs will affect previous decs[]
			continue
		if current is None:
			""" New set of parameters => store name """
			current = val[0]
			continue
																																				# Save parameter into dictionary
		varlist[nm] = val[:]
	"""
	We need to store the last declenson, otherwise it's lost
	If there is no empty line followed by a comment in the parser file
	"""
	if verb: print("End of file, saving parameters for", current, "...")
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
	if "PATH" not in decs[x].pars:
		print("No path provided, Assuming path is './'")
		decs[x].pars["PATH"] = ["./"]
	if "P2" not in decs[x].pars:
		print("P2 is missing, will be computed")
		if "P0" in decs[x].pars:
			if verb : print("P0 is",	decs[x].pars["P0"])
			if  "P1" in decs[x].pars:
				#~ print("P1 is",	decs[x].pars["P1"])
				# TODO: Not guessable if both attributes are array
				# TODO: Gues if one attribute is array
				#~ decs[x].pars["P2"] = list()
				#~ decs[x].pars["P2"] =
				decs[x].pars["P2"] = [round(1 -
															float(decs[x].pars["P0"][0]) -
															float(decs[x].pars["P1"][0]), 4)]
				if verb: print("So P2 is",	decs[x].pars["P2"])
			else:
				raise NameError("You need to define at least two of 'P0', 'P1' and 'P3'")
	#~ print (vars(decs[x]))

decnames = list(decs.keys())
print("done\n")

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
		if verb : print(roll, " Saving map", len(maps)+1)
		maps.append(mymap.pars.copy())

	def checkpar (mymap, maps, par, parnames, roll, depth, skip=False):
		depth += 1
		par = parnames[depth-1]
		roll=roll+">"+par

		if len(mymap.pars[par]) > 1:
			""" Multiple values for parameter 'par' """
			values = mymap.pars[par]																					# Storing the values to restore them later
			if verb : print(roll, "= ", values)
			for x in values:
				#~ if x == values[-1]: print("Last value: SKIP!!!")
				if verb : print(roll, "=", x)
				localmap = deepcopy(mymap)																			# We work on a temporary copy of the parameter set
				localmap.pars[par] =  [x]																				# Now parameter 'par' has a single value
				#~ if verb : print(roll, "depth", depth, "/", len(parnames))
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
			if verb : print(roll, "<< restoring")
			mymap.pars[par] = values																					# Restoring the initial valueS of the parameter
		else:
			""" Only one value for this param """
			if verb : print(roll);
			if depth < len(mymap.pars):
				""" This is NOT the last parameter """
				res = checkpar(mymap=mymap, maps=maps, par=par,									# Need to check for the other parameters
												parnames=parnames, roll=roll, depth=depth)
				maps = res['maps']
				mymap = res['mymap']																						# Updating values from the resukt of checkpar()
				skip = res['skip']
			#~ if verb : print(roll, "depth", depth, "of", len(parnames))
			if (depth == (len(parnames) -1)) and not skip:
				""" This is the last parameter and
						the map has not been saved yet
				"""
				savemap(mymap, maps, roll)																			# Save
				skip=False																											# Next save should not be skipped (start from scratch)
			#~ if verb : print(roll, "\t", par, "= ", mymap.pars[par])
		return({'maps':maps, 'mymap':mymap, "skip":skip})										# End of the function, returning object as a dict
	#~ if recurs is False: print("Unrolling...")


	if verb : print(roll, "Checking for multiple values...")
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
	maps = deepcopy(res['maps']);																					# Getting the results back
	mymap = res["mymap"];



	if verb : print(roll, "Leaving function with", len(maps), "maps")
	return({'maps':maps, 'mymap':mymap})


maps = {}


for dec in sorted(decnames):
	if verb: print("unrolling for", dec)
	declen = None
	res = None
	declen = decs[dec]
	res = unroll(declen)
	maps[dec] = res['maps']


#~ print("Final maps are")
#~ for x in sorted(maps):
	#~ for m in maps[x]:
		#~ tmp = {k: m[k] for k in ("P0", "P1", "X_SIZE", 'Q11', 'Q22')}
		#~ pprint.pprint(tmp, width=4)



mapnames = list(maps.keys())



def launchJob(cmd):
	"A single-arument function to launch a command"
	print("\nLaunching\n", cmd)
	subprocess.call( cmd, shell = True)


def launch (infile, executable, filename, path="./"):
	""" Launch the TLG program, redirecting stdout and stderr to
			corresponding files
	"""

	if not os.path.exists(path+"/OUT/"):
		print(path+"/OUT/ does not exist, creating it")
		os.makedirs(path+"/OUT/")
	if not os.path.exists(path+"/LOGS/"):
		print(path+"/LOGS/ does not exist, creating it")
		os.makedirs(path+"/LOGS/")
	cmd = executable + " " + infile + " 1> "+ path + "/LOGS/" + filename + ".out 2> " + path + "/LOGS/" + filename +".err"
	# TODO: Implement custom OUT path
	print("redying command", cmd)																					# Assigning the job to the pool of CPUs
	return(cmd)

#
# Printing the maps into .in files
#
# A dedicated function:
#
def map2in( mapdict, mapname, mapid=None, suffix=".in", path="./", cmd="nope"):
	"This prints a passed string to a passed file"
	mymap = mapdict
	name = mapname
	path = os.path.expanduser(path)																				# Replaces "~"
	path = os.path.normpath(path)																					# Replaces "./" "../ etc
	path = os.path.abspath(path)																					# Not sure if useful
	if verb : print("path is ", path);
	if mapid is not None:
		""" There is a map replicate ID, should add it to the name """
		name = name + "_" +str(mapid).zfill(4)															# 4 digits -> up to 9999 maps
	# Opening file
	if not os.path.exists(path+"/IN/"):
		""" IN/ directory is missing, need to create it first """
		print(path+"/IN/ does not exist, creating it")
		os.makedirs(path+"/IN/")
	filename = path + "/IN/" + name + suffix
	if verb : print("filename is", filename)
	file = open(filename, "w")
	# Writing content
	file.write("[NAME:"+ name +"] => Name of the generated landscape\n")
	file.write("[X_SIZE:" + str(int(float(mymap["X_SIZE"][0]))) + "]X[Y_SIZE:" + str(int(float(mymap["Y_SIZE"][0]))) + "] => size of the landscape\n")
	file.write("[P1:" + str(float(mymap["P1"][0])) + "] => proportion of type 1 (agricultural)\n")
	file.write("[P2:" + str(float(mymap["P2"][0])) + "] => proportion of type 2 (urban)\n")
	file.write("[Q11:" + str(float(mymap["Q11"][0])) + "] => P(11|1*)\n")
	file.write("[Q22:"+ str(float(mymap["Q22"][0])) + "] => P(22|2*)\n")
	file.write("[MAX_ITERATIONS:" + str(int(float(mymap["MAX_ITERATIONS"][0]))) + "] => Max number of iterations\n")
	file.write("[ERROR_THRESHOLD:"+ str(int(float(mymap["ERROR_THRESHOLD"][0]))) + "] => Min value of delta to keep going\n")
	file.write("[METHOD:"+ mymap["METHOD"][0] + "] => Method to compute delta\n")
	file.write("[SEED:"+ str(int(float(mymap["SEED"][0]))) + "] => Random seed number, set to 0 for random\n")
	# Closing file
	file.close()
	if not dry:
		""" Parameter --dryrun not set """
		cmd.append(launch(filename, "tlg-core", filename=name, path=path))							# Actually launches TLG
	return;

#
# Looping over all maps
#
print("\n")



cmd = list()																														# Will contain all commands to launch the runs

for x in sorted(maps):
	i = 0
	for m in maps[x]:
		i += 1
		reps = list(range(int(m["REPLICATES"][0])))													# Create a list 0:REPLICATES
		reps = [x+1 for x in reps] 																					# add 1 to reps : 1:(REPLICATES +1)
		if verb: print("Creating '.in' file(s) for map",
						str(i).zfill(3), "declension " + x,
						"(", m["REPLICATES"][0], "replicates)")
		for r in reps :
			# TODO: Implement offset for replicates (in case we want additional maps
			map2in(mapdict=m, mapname=x+"_"+str(i).zfill(3), mapid=r, path=m["PATH"][0],  cmd=cmd)


""" When every job is listed, we just have to start the worker """
				
start = time.time()

for cm in cmd:
		q.put(cm)																														# Put a worker at work

q.join()																																# Wait until the thread terminates.

"""
Writing down a line in log.txt to remember how long the actual
running took
"""
f=open("log.txt", "w")
text = "running parameters set in " +  thefile +  "took: " + str(time.time() - start)
f.write(text)
f.close()
