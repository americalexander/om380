from Itinerary import Itinerary
from Arcs import TripStartArc,NextDayArc

class ItineraryReader:
	def __init__(self, file):
		self.f = open(file)
	
	def read(self, flights, deps, sinks):
		itins = []
		self.f.readline()
		line = self.f.readline()
		while line is not '':
			args = line.split(',')
			
			ff = flights.get(int(args[0]), None)
			sf = flights.get(int(args[1]), None)
			psgrs = int(args[2])
			itin = Itinerary(ff, sf, psgrs)
			itins.append(itin)
			line = self.f.readline()
		self.f.close()
		
		for itin in itins:
			if itin.canceled():
				#Next-day flight arcs
				nd = NextDayArc(itin,sinks[itin.end().j])
				itin.outgoing.append(nd)
				itin.end().incoming.append(nd)
				
				#Itinerary arrival arcs
				for dep in deps.get(itin.j,[]):
					if dep.t > itin.t:
						sa = TripStartArc(itin,dep)
						itin.outgoing.append(sa)
						dep.incoming.append(sa)
			else:
				itin.ff.reduce(itin.psgrs)
				if itin.sf != None:
					itin.sf.reduce(itin.psgrs)
		
		return itins