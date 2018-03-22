#!/usr/bin/env python
from FlightReader import FlightReader as FReader
from ItineraryReader import ItineraryReader as IReader
from Arcs import *
from Flight import Flight
from Nodes import *
from Itinerary import Itinerary
import copy
import sys
import time
import heapq as pq

###############################
#
# I have totally abandoned hope for finishing this,
# so here's what you get:
#
#	functionally correct source code that runs well with small networks
#	an alternate method that uses topological search
#	all the data originally requested, except for the histograms
#		will print out at the end IF IT EVER FINISHES
#		which it will cuz the implementation is correct, but slow
#	You want histograms!? the buckets are in the psgrList and stopList
#		arrays. Have fun with that. If I had seen it end, I could have
#		implemented that functionality
#
# I am letting my partner down with how shitty this code is.
# May God have mercy on my soul.
#
#		~~William Alexander

def dijkstra(itin, nodes):
	#Dijkstra's algorithm
	labelTime = 0.0	#Time spent searching for the min
	dist = dict()	#distance map
	prev = dict()	#previous arc map
	dist[itin] = 0	#set source to dist 0
	q = copy.copy(nodes)	#make a copy of the nodes list for removal
	goal = itin.end()	#target node
	
	while q: #while not all nodes have been examined
		small = None
		tick = time.perf_counter() #start searching for min label
		for node in q:	#for each node in the queue
			if node in dist.keys():	#compare the size and take the smaller
				if small is None or dist.get(node, sys.maxsize) < dist.get(small, sys.maxsize):
					small = node
		labelTime += time.perf_counter() - tick #stop searching for min label
		if small is None or small is goal: #if end of reachable nodes or end of caring
			break	#we can give up here
		
		q.remove(small)	#remove the smallest element from q
		w = dist.get(small, sys.maxsize)	#get its distance from source
		
		#update all nodes reachable from this node
		for arc in small.outgoing:
			weight = w + arc.cost()	#get the alternate cost
			if dist.get(arc.j, sys.maxsize) > weight:	#if smaller, update
				dist[arc.j] = weight
				prev[arc.j] = arc
	
	#build the path from itin to sink nodes
	cur = goal	#start from the goal and work backwards
	path = []	#container of arcs in shortest path
	nd = False	#whether the trip is a next-day trip
	stops = 0	#number of connections
	while cur != itin:	#while the end hasn't been reached
		arc = prev.get(cur) #move backwards along the path
		
		#do some record-keeping checks
		if arc.__class__ == NextDayArc:
			nd = True
		elif arc.__class__ == ConnectionArc:
			stops+=1
		#add to the path then get the next node
		path.append(arc)
		cur = arc.i
	return list(reversed(path)), nd, stops, labelTime

def book(arcs, p):
	#Book as many passengers as possible
	for arc in arcs:
		p = arc.available(p)	#this effectively gets the min allowable bookings
	tc = 0	#travel cost for trip
	wc = 0	#waiting cost for trip
	cc = 0	#connection cost for trip
	
	for arc in arcs:
		#handle different cost types
		if arc.__class__   == Flight:
			tc += p * arc.cost()
		elif arc.__class__ == TripStartArc:
			wc += p * arc.cost()
		elif arc.__class__ == ConnectionArc:
			cc += p * arc.cost()
		elif arc.__class__ == NextDayArc:
			travel, wait, conn = arc.costBreakdown()
			tc += travel
			wc += wait
			cc += conn
		arc.reduce(p)	#remove available seats from arc
	return p, tc, wc, cc	#number booked, cost breakdown for itin

def topoSort(itins):
	#Get a topological ordering of all nodes
	S = itins	#list of all nodes with no incoming arcs
	order = []	#eventual container of topological order
	deadArcs = []	#arcs we've removed from the graph
	
	while S is not []:	#While there's still nodes to check
		n = S.pop()		#remove a node
		order.append(n)	#append it to the topo order
		
		for arc in n.outgoing:	#for each outgoing arc
			deadArcs.append(arc)	#remove arc from graph
			
			hasOther = False	#check if this arc now has indegree 0
			for inarc in arc.j.incoming:	#iterate through incoming links
				if inarc not in deadArcs:	#find one that isn't dead
					hasOther = True
					break
			
			if not hasOther:	#if the node has indegree 0
				S.append(arc.j)	#append to the list S
	return order

def topoSearch(itin, order):
	#given a topological ordering, find shortest paths
	order = order[order.index(itin):] #we only care about things with higher order
	prev = dict()	#previous arc map
	dist = dict()	#distance map
	dist[itin] = 0.0	#set source distance to 0
	
	for node in order: #for node in topo order
		if not dist.get(node,False):	#if the arc's distance is infinity
			continue	#skip over it (unreachable from the source)
		
		for arc in node.outgoing: #for each outgoing arc
			alt = arc.cost() + dist.get(node, None)	#get alternative distance
			if alt < dist.get(arc.j, sys.maxsize):	#if smaller, update
				dist[arc.j] = alt
				prev[arc.j] = arc
	
	#build the sequence of arcs in the shortest path 
	goal = itin.end()	#####For more details on this section, see the dijkstra's method
	cur = goal
	path = []
	nd = False
	stops = 0
	while cur != itin:
		arc = prev.get(cur)
		if arc.__class__ == NextDayArc:
			nd = True
		elif arc.__class__ == ConnectionArc:
			stops+=1
		path.append(arc)
		cur = arc.i
	return list(reversed(path)), nd, stops

def main():
	if len(sys.argv) < 3:
		print("Usage: ./Assignment2 flightFile itinFile [--topo]")
		return
	
	t0 = time.perf_counter()	#start of preprocessing time
	
	#read flight and itinerary data, set up network, net out capacity
	fr = FReader(sys.argv[1])	#flight reader object (see FlightReader.py)
	ir = IReader(sys.argv[2])	#itin reader object (see ItineraryREader.py)
	flights, deps, sinks, arrs = fr.read()	#read most of the nodes
	itins = ir.read(flights, deps, sinks)	#read itinerary nodes
	t1 = time.perf_counter()	#end of preprocessing time, start of sort
	
	#sort itineraries by departure time
	itins = sorted(itins, key=lambda itin: itin.t)	#sort itins by start time
	t2 = time.perf_counter()	#end sorting time
	
	
	#myopic rescheduling method
	disrupted = len(itins)		#count number of disrupted flights 
	revised = 0					#keep track of number of revised itins
	stopList = []				#keep track of number of stops in each itin
	psgrList = []				#keep track of number of psgrs in each itin
	dijkTime = 0.0				#keep track of time spent on dijkstra's
	labelTime = 0.0				#keep track of time searching for min label
	
	travelCost = 0				#cost for flight time
	waitingCost = 0				#cost for waiting at initial airport
	connectCost = 0				#cost for waiting at a connection airport
	
	#setup for topological method if the --topo argument is passed
	if sys.argv[3] is "--topo":
		to = True
		topo = topoSort(itins)	#get a topological ordering of the nodes
	else:
		to = False
		topo = []
	
	nodes = list(sinks.values()) #start compiling a list of all nodes (start w/ sinks)
	for v in arrs.values():
		nodes.extend(v)			#add all arrival nodes to list
	for v in deps.values():
		nodes.extend(v)			#add all departure nodes to list
	nodes.extend(itins)			#add all itinerary nodes
	
	for itinerary in itins:	#for each itin in order of departure time
		p = itinerary.psgrs	#get the desired number of passengers to be booked
		while p > 0:		#while the itinerary has unbooked passengers
			if not to:		#use dijkstra's to get shortest path
				tick = time.perf_counter()					#keep track of dijkstra time
				arcs, nd,cs,lt = dijkstra(itinerary, nodes) #see dijkstras method for details
				dijkTime += (time.perf_counter()-tick)		#add to total dijkstra time
				labelTime += lt								#add label search time
			else:			#use topological search to get shortest path
				arcs, nd, cs = topoSearch(itinerary, topo)
			
			booked, tc, wc, cc = book(arcs,p)	#book as many passengers as possible on this itin
			p -= booked	#decrement by how many have already been served
			psgrList.append(booked)	#keep track of passenger breakdown
			travelCost  += tc		#add to total travel cost
			waitingCost += wc		#add to total waiting cost
			connectCost += cc		#add to total connection cost
			
			if not nd:				#if not a next-day trip
				stopList.append(cs)	#keep track of stop breakdown
				revised += 1		#count an additional revised itin
		print("Done")	#proof we're not stuck
	
	#######################
	# OUTPUT ANSWERS HERE #
	#######################
	#Debug code below
	Nodes = len(nodes)
	#Debug code above
	nodes = StartNode.count + EndNode.count + SinkNode.count + Itinerary.count
	arcs  = Flight.count + ConnectionArc.count + \
		TripStartArc.count + TripEndArc.count + NextDayArc.count
	print("Disrupted itineraries:\t%d" % disrupted)
	#TODO: Histogram of psgrList
	print("Total number of nodes:\t%d\t" % (nodes))
	print("Total number of arcs: \t%d" % arcs)
	print("")
	print("Total cost:")
	print("\tTravel cost:\t\t%d" % travelCost)
	print("\tWaiting cost:\t\t%d" % waitingCost)
	print("\tConnection cost:\t%d" % connectCost)
	print("\t\t\t\t-----")
	print("\tSUM:\t\t\t%d" %(travelCost+waitingCost+connectCost))
	print("")
	print("Next-day passengers:\t%d" % NextDayArc.used)
	print("Bottlenecks:\t\t%d" % Flight.fullFlights)
	print("Revised itineraries:\t%d" % revised)
	#TODO: histogram of stopList
	print("")
	print("Preprocessing time:\t%f\tsecs" % (t1-t0))
	print("Itin. sorting time:\t%f\tsecs" % (t2-t1))
	print("Dijkstra's alg time:\t%f\tsecs" % dijkTime)
	print("Minimum label time:\t%f\tsecs" % labelTime)
	
	return 0

if __name__=="__main__":
	exit(main())