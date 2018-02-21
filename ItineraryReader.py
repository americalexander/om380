from Itinerary import Itinerary

class ItineraryReader:
	def __init__(self, file):
		self.f = open(file)
	
	def read(self, flights):
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
		return itins