#!/usr/bin/env python
from Arc import Arc
from ArcAdjacency import ArcAdjacencyList
import sys

def readNetwork(file):
	f = open(file)
	adjList = ArcAdjacencyList()
	line = f.readline()
	s = None
	t = None
	while line is not "":
		args = line.split("\t")
		if args[0] == "s":
			s = int(args[1])
		elif args[0] == "t":
			t = int(args[1])
			line = f.readline()
		else:
			i = int(args[0])
			j = int(args[1])
			c = int(args[2])
			if (i == s or j == t):
				if c > 0:
					
					adjList.addArc(i,j,c)
			else:
				adjList.addArc(i,j,c)
				adjList.addArc(i,j,c)
		line = f.readline()
	return adjList, s, t

def main():
	if len(sys.argv) < 2:
		print("Usage: Assignment3.py MaxFlow-img.txt")
		return 1
	filename = sys.argv[1]
	adjList, s, t = readNetwork(filename)
	
	return 0

if __name__ == "__main__":
	exit(main())