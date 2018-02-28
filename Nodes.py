class Node:
	def __init__(self, airport, time):
		self.j = airport
		self.t = time
		self.outgoing = []
		self.incoming = []

class StartNode(Node):
	count = 0
	def __init__(self, i,t):
		self.j = i
		self.t = t
		self.outgoing = []
		self.incoming = []
		StartNode.count += 1
	
	def __str__(self):
		return self.j + str(self.t)
	
	def __gt__(self,other):
		return self.t > other.t

class EndNode(Node):
	count = 0
	def __init__(self,j,t):
		self.j = j
		self.t = t
		self.outgoing = []
		self.incoming = []
		EndNode.count += 1
	
	def __str__(self):
		return self.j + str(self.t)
	
	def __gt__(self,other):
		return self.t > other.t

class SinkNode(Node):
	count = 0
	def __init__(self,airport):
		self.j = airport
		self.t = -1
		self.outgoing = []
		self.incoming = []
		SinkNode.count += 1
	
	def __gt__(self,other):
		return self.t > other.t
	
	def __str__(self):
		return "Sink "+self.j