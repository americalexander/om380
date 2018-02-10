class ArcAdjacencyList:
	def __init__(self):
		self.iNodes = dict()
		self.jNodes = dict()
	
	def addArc(self, arc):
		if self.iNodes.get(arc.i) == None:
			self.iNodes[arc.i] = []
		if self.jNodes.get(arc.j) == None:
			self.jNodes[arc.j] = []
		self.iNodes.get(arc.i).append(arc)
		self.jNodes.get(arc.j).append(arc)