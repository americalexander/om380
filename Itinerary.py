class Itinerary:
	def __init__(self,ff,sf,passengers):
		self.ff = ff
		self.sf = sf
		self.psgrs = passengers
	
	def __str__(self):
		if self.psgrs == 1:
			s = ''
		else:
			s = 's'
		orig = self.ff.orig
		if self.sf != None:
			dest = self.sf.dest
		else:
			dest = self.ff.dest
		return "%d passenger%s\tfrom %s to %s" % (self.psgrs, s, orig, dest)