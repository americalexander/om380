from Nodes import Node
class Itinerary(Node):
	count = 0
	def __init__(self,ff,sf,passengers, sink):
		self.ff = ff
		self.sf = sf
		self.psgrs = passengers
		self.j = ff.i
		self.t = ff.i.t
		self.outgoing = []
		self.incoming = []
		self.sink = sink
		Itinerary.count += 1
	
	def schedCost(self):
		fc = self.ff.cost()
		if self.sf == None:
			return fc
		else:
			sc = self.sf.cost()
			wc = self.sf.i.t - self.ff.j.t + 30
		return fc + sc + wc
	
	def canceled(self):
		return self.ff.canceled or (self.sf != None and self.sf.canceled)
	
	def __str__(self):
		if self.psgrs == 1:
			s = ''
		else:
			s = 's'
		orig = self.ff.i
		if self.sf != None:
			dest = self.sf.j
		else:
			dest = self.ff.j
		return "%d passenger%s\tfrom %s to %s\t%s" \
			% (self.psgrs, s, orig, dest, self.canceled())
	
	def end(self):
		return self.sink
	
	def __gt__(self,other):
		return self.t > other.t