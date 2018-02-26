#!/usr/bin/env python
from FlightReader import FlightReader as FReader
from ItineraryReader import ItineraryReader as IReader
from Arcs import *
from Flight import Flight
from Nodes import *
from Itinerary import Itinerary
import sys
import time

def dijkstra(itin):
	#TODO: Implement Dijkstra's algorithm
	labelTime = 0.0
	return [], False, 0, labelTime

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
		arc.reduce(p)
	return p, tc, wc, cc

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
	
	for itinerary in itins:
		p = itinerary.psgrs
		while p > 0:
			tick = time.perf_counter()
			arcs, nd,cs,lt = dijkstra(itinerary)
			dijkTime += (time.perf_counter()-tick)
			labelTime += lt
			
			booked, tc, wc, cc = book(arcs,p)
			p -= booked
			psgrList.append(booked)
			travelCost  += tc
			waitingCost += wc
			connectCost += cc
			if not nd:
				stopList.append(cs)
				revised += 1
	
	nodes = StartNode.count + EndNode.count + SinkNode.count + Itinerary.count
	arcs  = Flight.count + ConnectionArc.count + \
		TripStartArc.count + TripEndArc.count + NextDayArc.count
	print("Disrupted itineraries:\t%d" % disrupted)
	#TODO: Histogram of psgrList
	print("Total number of nodes:\t%d" % nodes)
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