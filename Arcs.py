from Itinerary import Itinerary
from Arc import Arc
from Nodes import SinkNode, EndNode, StartNode

class ConnectionArc(Arc):	#Intermediate Waiting Arc (Connection)
	count = 0
	def __init__(self,endNode,startNode):
		assert endNode.__class__ == EndNode
		assert startNode.__class__ == StartNode
		self.i = endNode
		self.j = startNode
		ConnectionArc.count += 1
	
	def cost(self):
		return self.j.t - self.i.t + 30
	
	def available(self,num):
		return num

class TripStartArc(Arc):	#Itinerary Arrival Arc
	count = 0
	def __init__(self,itinNode, startNode):
		assert itinNode.__class__ == Itinerary
		assert startNode.__class__ == StartNode
		self.i = itinNode
		self.j = startNode
		TripStartArc.count += 1
	
	def cost(self):
		return self.j.t - self.i.t
	
	def available(self, num):
		return num
	
	def reduce(self,num):
		pass

class TripEndArc(Arc):	#Itinerary End Arc
	count = 0
	def __init__(self,endNode, sinkNode):
		assert sinkNode.__class__ == SinkNode
		assert endNode.__class__ == EndNode
		self.i = endNode
		self.j = sinkNode
		TripEndArc.count += 1
	
	def cost(self):
		return 0
	
	def available(self, num):
		return num
	
	def reduce(self,num):
		pass

class NextDayArc(Arc):	#Next-Day Flight Arc
	count = 0
	used = 0
	def __init__(self,itinNode,sinkNode):
		assert itinNode.__class__ == Itinerary
		assert sinkNode.__class__ == SinkNode
		self.i = itinNode
		self.j = sinkNode
		NextDayArc.count += 1
	
	def cost(self):
		waitCost = 24*60
		return waitCost + self.i.schedCost()
	
	def available(self,num):
		return num
	
	def reduce(self, num):
		NextDayArc.used += num