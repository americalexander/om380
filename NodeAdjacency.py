class NodeAdjacencyList:
	def __init__(self):
		self.nodes = dict()
	
	def addArc(self, arc):
		if self.nodes.get(arc.i) == None:
			self.nodes[arc.i] = []
		if self.nodes.get(arc.j) == None:
			self.nodes[arc.j] = []
		self.nodes[arc.i].append(arc.j)
		self.nodes[arc.j].append(arc.i)
