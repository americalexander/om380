#!/usr/bin/env python
from FlightReader import FlightReader as FReader
from ItineraryReader import ItineraryReader as IReader
import sys

def main():
	if len(sys.argv) < 3:
		print("Usage: ./Assignment2 flightFile itinFile")
		return
	fr = FReader(sys.argv[1])
	ir = IReader(sys.argv[2])
	
	flights = fr.read()
	itins = ir.read(flights)
	
	print(str(len(flights))+"\t"+str(len(itins)))

if __name__=="__main__":
	main()