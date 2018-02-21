class Flight:
	def __init__(self, id, orig, dest, start, end, canceled, seats):
		self.id = id
		self.orig = orig
		self.dest = dest
		self.startTime = start
		self.endTime = end
		self.canceled = canceled
		self.seats = seats
	
	def __str__(self):
		if self.canceled:
			status = "CANCELD"
		else:
			status = "ON TIME"
		return "Flgt %d\tOrig %s\tDest %s\tDept %d\tArrv %d\tStat %s\tSeat %s" \
		% (self.id, \
		self.orig, \
		self.dest, \
		self.startTime, \
		self.endTime, \
		status, \
		self.seats)