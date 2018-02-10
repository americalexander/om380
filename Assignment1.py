#!/usr/bin/env python
from ArcReader import ArcReader
import sys
import time
import queue

def q1(list):
	q = queue.PriorityQueue()	#Keep a leaderboard of trust
	
	for node in list.jNodes.keys():	#For each trusted node
		q.put((-len(list.jNodes[node]),node))	#Add to the leaderboard
	
	maxTrust = []	#The first 20 entries of the leaderboard go here
	for i in range(20):	#Add them iteratively
		maxTrust.append(q.get())
	
	return maxTrust

def q2():
	pass

def q3(list, rev0):
	informed = {rev0[0]: True}	#informed users
	tt40 = -1	#days until 40% reached
	ttt = -1	#total days
	
	while len(rev0) > 0:	#While new opinions are posted
		ttt += 1	#Continue on for another day
		rev1 = []	#People becoming informed today
		
		for reviewer in rev0:	#For all the people that reviewed yesterday:
			outArcs = list.jNodes.get(reviewer,[])
			for trustArc in outArcs:	#People that trust that reviewer
				truster = trustArc.i
				if not informed.get(truster, False):	#and aren't already informed
					rev1.append(truster)				#will write a review today
					informed[truster] = True			#and are now informed
		
		if tt40 == -1 and len(informed)>30115:	#If 40% of people are now informed
			tt40 = ttt	#record the day this first occurred
		
		rev0 = rev1	#A new day dawns
	
	return tt40, ttt, (float(len(informed))/75289)

def q4():
	pass


def main():
	if len(sys.argv) < 2:
		print("Usage: ./Assignment1 TrustNetwork.txt")
		return
	r = ArcReader(sys.argv[1])
	array, list = r.read()
	
	## Question 1
	t0 = time.perf_counter()
	maxTrust = q1(list)
	t1 = time.perf_counter()
	
	print("MOST TRUSTED INDIVIDUALS")
	for tuple in maxTrust:
		print("Individual "+str(tuple[1]))
	
	print("Q1 Time: %s\tseconds\n" % str(t1-t0))
	
	## Question 2
	t1 = time.perf_counter()
	q2()
	t2 = time.perf_counter()
	print("Q2 Time: %s\tseconds\n" % str(t2-t1))
	
	## Question 3
	t2 = time.perf_counter()
	tt40, ttt, iff = q3(list, [maxTrust[0][1]])
	t3 = time.perf_counter()
	
	print("INFORMATION PROPAGATION")
	print("Days to 40 percent informed:\t%d" % tt40)
	print("Days to propagation end:\t%d" % ttt)
	print("Final fraction informed:\t%4f" % iff)
	print("Q3 Time: %s\tseconds\n" % str(t3-t2))
	
	## Question 4
	t3 = time.perf_counter()
	q4()
	t4 = time.perf_counter()
	print("Q4 Time: %s\tseconds" % str(t4-t3))


if __name__ == "__main__":
	main()