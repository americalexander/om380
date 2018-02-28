from Arc import Arc
from Nodes import StartNode, EndNode
from sys import maxsize as infinity
class Flight(Arc):
	fullFlights = 0
	count = 0
	def __init__(self, id, orig, dest, canceled, seats):
		assert orig.__class__ == StartNode
		assert dest.__class__ == EndNode
		self.id = id
		self.i = orig
		self.j = dest
		self.canceled = canceled
		self.seats = seats
		Flight.count += 1
	
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
		if self.seats <= 0:
			return infinity
		return self.j.t - self.i.t
	
	def available(self,number):
		d = self.seats - number
		if d > 0:
			return number
		else:
			return number + d
	
	def reduce(self,num):
		assert num <= self.seats
		self.seats -= num
		if self.seats == 0:
			Flight.fullFlights += 1