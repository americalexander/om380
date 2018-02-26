from Itinerary import Itinerary
from Arc import Arc
from Nodes import SinkNode, EndNode, StartNode

class ConnectionArc(Arc):	#Intermediate Waiting Arc (Connection)
	def __init__(self,endNode,startNode):
		assert endNode.__class__ == EndNode
		assert startNode.__class__ == StartNode
		self.i = endNode
		self.j = startNode
	
	def cost(self):
		return self.j.t - self.i.t + 30
	
	def reduce(self,num):
		return num

class TripStartArc(Arc):	#Itinerary Arrival Arc
	def __init__(self,itinNode, startNode):
		assert itinNode.__class__ == Itinerary
		assert startNode.__class__ == StartNode
		self.i = itinNode
		self.j = startNode
	
	def cost(self):
		return self.j.t - self.i.t
	
	def reduce(self, num):
		return num

class TripEndArc(Arc):	#Itinerary End Arc
	def __init__(self,endNode, sinkNode):
		assert sinkNode.__class__ == SinkNode
		assert endNode.__class__ == EndNode
		self.i = endNode
		self.j = sinkNode
	
	def cost(self):
		return 0
	
	def reduce(self, num):
		return num

class NextDayArc(Arc):	#Next-Day Flight Arc
	def __init__(self,itinNode,sinkNode):
		assert itinNode.__class__ == Itinerary
		assert sinkNode.__class__ == SinkNode
		self.i = itinNode
		self.j = sinkNode
	
	def cost(self):
		waitCost = 24*60
		return waitCost + self.i.schedCost()