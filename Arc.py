class Arc:
	def __init__(self, i, j, capacity):
		self.i = i
		self.j = j
		self.capacity = capacity
	
	def __str__(self):
		return ""+str(self.i)+","+str(self.j)+","+str(self.capacity)