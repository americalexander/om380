class Flight:
	def __init__(self, id, orig, dest, start, end, canceled, seats):
		self.id = id
		self.orig = orig
		self.dest = dest
		self.startTime = start
		self.endTime = end
		self.canceled = canceled
		self.seats = seats