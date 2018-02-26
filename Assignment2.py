#!/usr/bin/env python
from FlightReader import FlightReader as FReader
from ItineraryReader import ItineraryReader as IReader
import sys
import time

def mapNetwork(flights, itins):
	arrs = dict()
	deps = dict()
	for flight in flights:
		da = deps.get(flight.orig, [])
		aa = arrs.get(flight.dest, [])
		da.append(flight)
		aa.append(flight)
		deps[flight.orig] = da
		arrs[flight.dest] = aa
	

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
	flights, deps, sinks = fr.read()
	itins = ir.read(flights, deps, sinks)
	t1 = time.perf_counter()
	
	#TODO: sort itineraries by departure time here
	
	t2 = time.perf_counter()
	
	#TODO: Dijkstra's algorithm goes here
	
	t3 = time.perf_counter()
	

	
	return 0

if __name__=="__main__":
	exit(main())