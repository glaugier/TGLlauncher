TLG.py
===========

A launcher for the Ternary Landscape Generator program.

Usage
-----

```shell
	TLG.py parset.txt
```
or
```shell
	TLG.py parsets/*    # CURRENTLY BROKEN
```
assuming directory 'parsets' holds input files such as parset.txt

Parameter list:
---------------

`#: Comment`			(line ignored)

`NAME:string`			(Run name, will be used to create the .in and output file)

`X_SIZE:int`			(Landscape width (in px))

`Y_SIZE:int`			(Landscape height (in px) Assumed equal to X_SIZE if missing (squared landscape))

`P0:real*`				(Proportion of type 0 habitat)

`P1:real*`				(Proportion of type 1 habitat)

`P2:real*`				(Prop. of type 2, computed if missing, better let the program do the math)

`Q11:real*`				(P(11|1*) )

`Q22:real*`				(P(11|1*) )

`MAX_ITERATIONS:int`	(Maximum number of iteration if did not converge)

`ERROR_THRESHOLD:real`	(Max delta value)

`METHOD:string`			(Name of the method usedd to compute delta)

`SEED:int`				(Seed number for random generator, default to zero: random seed)

`PATH:string`			(Optional: path where to generate files, defaults to `./`)

`REPLICATES:int`		(Optional: number of replicate for each parapeter combo, defaults to 1)

An asterisk `*` indicates possible multiple values separated by `:`

Several such "declensions" can be put in a single "parset" file, separated by an empty line.

Features
--------

 + Read data from "parset" file
   + All parameters are defined by a line, starting with a name, a colon, followed by values separated by columns
   + Lines starting with `#:` are ignored (comments)
   + Unrecognised parameters are read and stored but not used (Should not crash the program)
 + (Partial) guessing of missing parameters:
  + P2 is guessed from `P1` and `P2` if missing
 + `REPLICATES` is assumed to be 1 if missing
 + Multiple values for parameters: All combinations will be created
 + A general path to where to save the files
  + Create the required Architecture (IN/ OUT/ LOG/) if the directories are missing
  + Create ".in" files ready to be used by TLG
   + File name as <NAME>_<Map number>_<Replicate number>.in where
    - <NAME> is the value of parameter `NAME` in the parset file
    - <Map number> is an arbitrary number given to each of the map sets derived from a declension set
    - <Replicate number> is the replicate ID (4-digit integer)
 + Launches the actual TLG program for each .in file generated
  + Processes are launched in parallel (multithreading)
  + Automatically choses number of CPUs (n-1, where n is the number of the machine)

Requirements
---------------

 + Requires tgl-core v1.0.8 or higher installed (_i.e._ in the $PATH)

Troubleshooting
---------------

 + Ignoring OUT/ again when generating the files...
 + Broken feature: Using several parset files eg: parset/*
 
TODO
----

 + Handle more possibilities (missing values)
 + Implement offset for replicates
 + Option for only generating the .in files
  + More CLI arguments
   + Non-verbose mode
   + Handle custom path to exectutable
   + Custom number of simultaneous CPUs

  
