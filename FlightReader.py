from Flight import Flight
from Nodes import StartNode, EndNode, SinkNode
from Arcs import ConnectionArc, TripEndArc

class FlightReader:
	def __init__(self, file):
		self.f = open(file)
	
	def mapArcs(_,arrs,deps,sinks):
		for airport in arrs.keys():
			arrivals = arrs.get(airport,[])
			departures = deps.get(airport,[])
			for arrival in arrivals:
				#Itinerary end arcs
				s = sinks[airport]
				e = TripEndArc(arrival, s)
				arrival.outgoing.append(e)
				s.incoming.append(e)
				
				#Intermediate waiting arcs
				for departure in departures:
					if departure.t >= arrival.t:
						c = ConnectionArc(arrival, departure)
						arrival.outgoing.append(c)
						departure.incoming.append(c)
	
	def read(self):
		flights = dict()
		arrs = dict()
		deps = dict()
		sinks = dict()
		
		self.f.readline()
		line = self.f.readline()
		while line is not '':
			args = line.split(',')
			start = StartNode(args[2],int(args[5]))
			end = EndNode(args[3],int(args[7]))
			
			#Map from airport to list of arrivals
			a = arrs.get(args[3], [])
			a.append(end)
			arrs[args[3]] = a
			
			#Map from airport to list of departures
			d = deps.get(args[2],[])
			d.append(start)
			deps[args[2]] = d
			
			#Map from airport to list of sink nodes
			s = sinks.get(args[3],None)
			if s == None:
				sinks[args[3]] = SinkNode(args[3])
			
			#Construct flight arcs
			flight = Flight(int(args[0]),#ID \
				start, end,
				bool(int(args[8])), #canceled \
				int(args[9]) #seats \
			)
			#Append to the node-arc adjacency lists
			start.outgoing.append(flight)
			end.incoming.append(flight)
			
			flights[int(args[0])] = flight
			line = self.f.readline()
		self.f.close()
		
		self.mapArcs(arrs,deps,sinks)
		
		return flights, deps, sinks, arrs