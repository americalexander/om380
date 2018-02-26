class Node:
	def __init__(self, airport, time):
		self.j = airport
		self.t = time
		self.outgoing = []
		self.incoming = []

class StartNode(Node):
	def __init__(self, i,t):
		self.j = i
		self.t = t
		self.outgoing = []
		self.incoming = []
	
	def __str__(self):
		return self.j + str(self.t)

class EndNode(Node):
	def __init__(self,j,t):
		self.j = j
		self.t = t
		self.outgoing = []
		self.incoming = []
	
	def __str__(self):
		return self.j + str(self.t)

class SinkNode(Node):
	def __init__(self,airport):
		self.j = airport
		self.t = -1
		self.outgoing = []
		self.incoming = []