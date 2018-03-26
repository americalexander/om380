#!/usr/bin/env python
from Arc import Arc
from ArcAdjacency import ArcAdjacencyList
import sys
import copy
import time

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
	#Shortest Augmenting Path algorithm
	x = 0
	d = dists(adjList,t) #get exact distance labels
	i = s
	pred = dict()
	arcscans = 0
	augments = 0
	advances = 0
	retreats = 0
	
	while d[s] < len(adjList.iNodes) + 1: #while d(s) < n
		hasArc = False	#condition of having an admissible arc
		for j in adjList.getOutgoing(i):
			arcscans += 1
			if d[i] != d[j] + 1 or adjList.getOutgoing(i)[j] <= 0: #if not admissible:
				continue
			hasArc = True	#we have found at least one admissible arc
			
			#advance(i, j)
			advances += 1
			pred[j] = i
			i = j
			
			if j == t:
				#augment()
				augments += 1
				path = [t]
				cur = t
				delta = 65536
				while cur is not s:	#build a path from s to t using the pred labels
					delta = min(delta, adjList.getOutgoing(pred[cur])[cur])	#restricting flow
					cur = pred[cur]
					path = [cur] + path
				x += delta
				for i in range(1,len(path)):	#shift flow from the forward arc to the reverse
					nv = adjList.getOutgoing(path[i-1]).get(path[i], None) - delta
					adjList.getOutgoing(path[i-1])[path[i]] = nv
					nv = adjList.getOutgoing(path[i]).get(path[i-1], 0) + delta
					adjList.getOutgoing(path[i])[path[i-1]] = nv
				i = s
			break
		
		if not hasArc:
			#retreat(i)
			retreats += 1
			tempd = 65536
			tempj = -1
			#get the minimum distance label possible
			for j in adjList.getOutgoing(i):
				arcscans += 1
				rij = adjList.getOutgoing(i)[j]
				if rij > 0 and d[j] < tempd:
					tempd = d[j]
					tempj = j
			tempd += 1
			d[i] = tempd	#d(i) is the min neighbor d + 1
			if i != s:
				i = pred[i]	#alter the pred mapping
	return x, arcscans, augments, advances, retreats

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
				adjList.addArc(j,i,c)
		
		line = f.readline()
	return adjList, s, t

def reachability(adjList,s):
	#Breadth-first search
	visited = set()
	pred = dict()
	pred[s] = None
	q = [s]
	visited.add(s)
	
	while len(q) > 0:
		i = q.pop()
		for j in adjList.getOutgoing(i):
			if j in visited or adjList.getOutgoing(i)[j] <=0:
				continue
			visited.add(j)
			pred[j] = i
			q.append(j)
			
	return visited

def calcA(S,s,base):
	a = 0
	for node in S:
		a += base.getOutgoing(s).get(node, 0)
	return a

def calcB(T,t,base):
	b = 0
	for node in T:
		b += base.getIncoming(t).get(node,0)
	return b

def main():
	if len(sys.argv) < 2:
		print("Usage: Assignment3.py MaxFlow-img.txt")
		return 1
	
	#read in the network
	filename = sys.argv[1]
	adjList, s, t = readNetwork(filename)
	base = copy.deepcopy(adjList)
	
	tic = time.perf_counter()	#start of shortest path algorithm
	x, arcscans, augments, advances, retreats = sap(adjList,s,t)
	
	#now that we have our S/T cut created, map that into sets of nodes
	S = reachability(adjList, s) #use the reachability algorithm (BFS)
	T = set()
	for node in adjList.iNodes:	#every node not in S should be in T
		if node not in S:
			T.add(node)
	a = calcA(S,s, base)
	b = calcB(T,t, base)
	#output results
	print("Time taken: "+str(time.perf_counter() - tic))
	print("Number of augments: "+str(augments))
	print("Number of advances: "+str(advances))
	print("Number of retreats: "+str(retreats))
	print("Total flow sent:    "+str(x))
	
	print("Number of foreground pixels: "+str(len(S)-1))
	print("Number of background pixels: "+str(len(adjList.iNodes)-(len(S))-1))
	print("Total Likelihood: "+(str(a+b)))
	
	return 0

if __name__ == "__main__":
	exit(main())