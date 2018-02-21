from Flight import Flight

class FlightReader:
	def __init__(self, file):
		self.f = open(file)
	
	def read(self):
		flights = dict()
		self.f.readline()
		line = self.f.readline()
		while line is not '':
			args = line.split(',')
			flight = Flight(int(args[0]),#ID \
				args[2], #orig \
				args[3], #dest \
				int(args[5]), #dep \
				int(args[7]), #arr \
				bool(int(args[8])), #canceled \
				int(args[9]) #seats \
			)
			flights[int(args[0])] = flight
			line = self.f.readline()
		self.f.close()
		return flights