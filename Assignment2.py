#!/usr/bin/env python
from FlightReader import FlightReader as FReader
from ItineraryReader import ItineraryReader as IReader
import sys
import time

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
	#read flight and itinerary data
	fr = FReader(sys.argv[1])
	ir = IReader(sys.argv[2])
	flights = fr.read()
	itins = ir.read(flights)
	
	#TODO: set up network here
	
	#TODO: net capacity usage for unaffected passengers here
	
	t1 = time.perf_counter()
	
	#TODO: sort itineraries by departure time here
	
	t2 = time.perf_counter()
	
	#TODO: Dijkstra's algorithm goes here
	
	t3 = time.perf_counter()
	

	
	return 0

if __name__=="__main__":
	exit(main())