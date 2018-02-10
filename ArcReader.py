from Arc import Arc
from ArcArray import ArcArray
from ArcAdjacency import ArcAdjacencyList
from NodeAdjacency import NodeAdjacencyList

class ArcReader:
	def __init__(self, file):
		self.f = open(file)
	
	def read(self):
		array = ArcArray()
		adjList = ArcAdjacencyList()
		line = self.f.readline()
		nodeList = NodeAdjacencyList()
		
		while line != "":
			while line[0] is "#":
				line = self.f.readline()
			args = line.split("\t")
			arc = Arc(int(args[0]),int(args[1]),int(args[2]))
			array.addArc(arc)
			adjList.addArc(arc)
			nodeList.addArc(arc)
			
			line = self.f.readline()
		self.f.close()
		return array, adjList, nodeList