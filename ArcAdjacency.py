class ArcAdjacencyList:
	def __init__(self):
		self.iNodes = dict()
		self.jNodes = dict()
	
	def addArc(self, i, j, c):
		self.iNodes.setdefault(i, dict())[j] = c
		self.jNodes.setdefault(j, dict())[i] = c
	
	def getOutgoing(self, node):
		return self.iNodes[node]
	
	def getIncoming(self, node):
		return self.jNodes.get(node, [])