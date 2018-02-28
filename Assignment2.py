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

def dijkstra(itin, nodes):
	#Dijkstra's algorithm
	labelTime = 0.0
	dist = dict()
	prev = dict()
	dist[itin] = 0
	q = copy.copy(nodes)
	goal = itin.end()
	while q:
		small = None
		tick = time.perf_counter()
		for node in q:
			if node in dist.keys():
				if small is None or dist.get(node, sys.maxsize) < dist.get(small, sys.maxsize):
					small = node
		labelTime += time.perf_counter() - tick
		if small is None or small is goal:
			break
		
		q.remove(small)
		w = dist.get(small, sys.maxsize)
		
		for arc in small.outgoing:
			weight = w + arc.cost()
			if dist.get(arc.j, sys.maxsize) > weight:
				dist[arc.j] = weight
				prev[arc.j] = arc
	
	cur = goal
	path = []
	nd = False
	stops = 0
	while cur != itin:
		arc = prev.get(cur)
		if arc is None:
			pass#print(path)
		if arc.__class__ == NextDayArc:
			nd = True
		elif arc.__class__ == ConnectionArc:
			stops+=1
		path.append(arc)
		cur = arc.i
	return list(reversed(path)), nd, stops, labelTime

def book(arcs, p):
	#Book as many passengers as possible
	for arc in arcs:
		p = arc.available(p)
	tc = 0
	wc = 0
	cc = 0
	for arc in arcs:
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
		arc.reduce(p)
	return p, tc, wc, cc

def topoSort(itins):
	S = itins
	order = []
	deadArcs = []
	while S is not []:
		n = S.pop()
		order.append(n)
		for arc in n.outgoing:
			deadArcs.append(arc)
			hasOther = False
			for inarc in arc.j.incoming:
				if inarc not in deadArcs:
					hasOther = True
					break
			if not hasOther:
				S.append(arc.j)
	return order

def topoSearch(itin, order):
	order = order[order.index(itin):]
	prev = dict()
	dist = dict()
	dist[itin] = 0.0
	for node in order:
		if not dist.get(node,False):
			continue
		for arc in node.outgoing:
			alt = arc.cost() + dist.get(node, None)
			if alt < dist.get(arc.j, sys.maxsize):
				dist[arc.j] = alt
				prev[arc.j] = arc
	
	goal = itin.end()
	cur = goal
	path = []
	nd = False
	stops = 0
	while cur != itin:
		arc = prev.get(cur)
		if arc is None:
			pass#print(path)
		if arc.__class__ == NextDayArc:
			nd = True
		elif arc.__class__ == ConnectionArc:
			stops+=1
		path.append(arc)
		cur = arc.i
	return list(reversed(path)), nd, stops

def main():
	if len(sys.argv) < 3:
		print("Usage: ./Assignment2 flightFile itinFile")
		return
	
	disruptedItineraries = []
	revisedItineraries = []
	totalCost = 0
	nextDayPsgrs = 0
	fullFlights = 0
	labeled = 0
	minLTime = 0
	t0 = time.perf_counter()
	
	#read flight and itinerary data, set up network, net out capacity
	fr = FReader(sys.argv[1])
	ir = IReader(sys.argv[2])
	flights, deps, sinks, arrs = fr.read()
	itins = ir.read(flights, deps, sinks)
	t1 = time.perf_counter()
	
	#sort itineraries by departure time
	itins = sorted(itins, key=lambda itin: itin.t)
	t2 = time.perf_counter()
	
	
	#myopic rescheduling method
	disrupted = len(itins)
	revised = 0
	stopList = []
	psgrList = []
	dijkTime = 0.0
	labelTime = 0.0
	
	travelCost = 0
	waitingCost = 0
	connectCost = 0
	
	if sys.argv[3] is "--topo":
		to = True
		topo = topoSort(itins)
	else:
		to = False
		topo = []
	
	nodes = list(sinks.values())
	for v in arrs.values():
		nodes.extend(v)
	for v in deps.values():
		nodes.extend(v)
	nodes.extend(itins)
	#print(len(nodes))
	for itinerary in itins:
		#print(itinerary in nodes)
		p = itinerary.psgrs
		while p > 0:
			if not to:
				tick = time.perf_counter()
				arcs, nd,cs,lt = dijkstra(itinerary, nodes)
				dijkTime += (time.perf_counter()-tick)
				labelTime += lt
			else:
				arcs, nd, cs = topoSearch(itinerary, topo)
			#print(arcs)
			#print(p)
			booked, tc, wc, cc = book(arcs,p)
			p -= booked
			psgrList.append(booked)
			travelCost  += tc
			waitingCost += wc
			connectCost += cc
			if not nd:
				stopList.append(cs)
				revised += 1
		print("Done")
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