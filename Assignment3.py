#!/usr/bin/env python
from Arc import Arc
from ArcAdjacency import ArcAdjacencyList
import sys

def dists(adjList, t):
	#Breadth-first search
	visited = set()
	pred = dict()
	pred[t] = None
	dists = dict()
	q = [t]
	dists[t] = 0
	visited.add(t)
	
	while len(q) > 0:
		j = q.pop()
		for i in adjList.getIncoming(j):
			if i in visited:
				continue
			visited.add(i)
			pred[i] = j
			dists[i] = dists[j] + 1
			q.append(i)
	
	return dists

def sap(adjList,s,t):
	x = 0
	d = dists(adjList,t)
	i = s
	pred = dict()
	
	while d(s) < len(adjList) + 1:
		hasArc = False
		for j in adjList.getOutgoing(i):
			if d[i] != d[j] + 1: #if not admissible:
				continue
			hasArc = True
			#advance(i, j)
			pred[j] = i
			i = j
			
			if j == t:
				#augment()
				i = s
			break
		if not hasArc:
			pass
			#retreat(i)

def readNetwork(file):
	f = open(file)
	adjList = ArcAdjacencyList()
	line = f.readline()
	s = None
	t = None
	while line is not "":
		args = line.split("\t")
		if args[0] == "s": #identify supersource
			s = int(args[1])
		elif args[0] == "t": #identify supersink
			t = int(args[1])
			line = f.readline() #skip the break line
		else:
			i = int(args[0])	#parse arc info
			j = int(args[1])
			c = int(args[2])
			if (i == s or j == t): #if this is a source/sink arc
				if c > 0:	#and it isn't zero capacity
					adjList.addArc(i,j,c)	#add to the network
			else:	#otherwise, add two arcs to the residual net
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
	
	sap(adjList,s,t)
	
	return 0

if __name__ == "__main__":
	exit(main())