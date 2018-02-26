from Arc import Arc
from Nodes import StartNode, EndNode
class Flight(Arc):
	def __init__(self, id, orig, dest, canceled, seats):
		assert orig.__class__ == StartNode
		assert dest.__class__ == EndNode
		self.id = id
		self.i = orig
		self.j = dest
		self.canceled = canceled
		self.seats = seats
	
	def __str__(self):
		if self.canceled:
			status = "CANCELD"
		else:
			status = "ON TIME"
		return "Flgt %d\tOrig %s\tDest %s\tStat %s\tSeat %s" \
		% (self.id, \
		self.i, \
		self.j, \
		self.i.t, \
		self.j.t, \
		status, \
		self.seats)
	
	def cost(self):
		return self.endTime - self.startTime
	
	def reduce(self,number):
		d = self.seats - number
		assert d >= 0
		self.seats = d