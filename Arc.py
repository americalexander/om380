class Arc:
	def __init__(self, id, i, j):
		self.i = i
		self.j = j
		self.id = id
	
	def __str__(self):
		return ""+str(self.id)+","+str(self.i)+","+str(self.j)