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
	TLG.py parsets/*
```
assuming directory 'parsets' holds input files such as parset.txt

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
	+ Create ".in" files ready to be used by TLG
	
		+ File name as <NAME>_<Map number>_<Replicate number>.in where

			+ <NAME> is the value of parameter `NAME` in the parset file
			+ <Map number> is an arbitrary number given to each of the map sets derived from a declension set
			+ <Replicate number> is the replicate ID (4-digit integer)

Troubleshooting
---------------

 + Not working yet.

TODO
----

 + Handle more possibilities (missing values)
 + Implement offset for replicates
 + Actually launch TLG .in files

