class ArcAdjacencyList:
	def __init__(self):
		self.iNodes = dict()
	
	def addArc(self, arc):
		if self.iNodes.get(arc.i) == None:
			self.iNodes[arc.i] = []
		self.iNodes.get(arc.i).append(arc)