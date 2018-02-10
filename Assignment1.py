#!/usr/bin/env python
from ArcReader import ArcReader
import sys
import time
import queue

def q1(list):
	q = queue.PriorityQueue()
	for node in list.jNodes.keys():
		q.put((-len(list.jNodes[node]),node))
	maxTrust = []
	for i in range(20):
		maxTrust.append(q.get())
	return maxTrust

def q2():
	pass

def q3():
	pass

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
	print("MOST TRUSTED:")
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
	q3()
	t3 = time.perf_counter()
	print("Q3 Time: %s\tseconds\n" % str(t3-t2))
	
	## Question 4
	t3 = time.perf_counter()
	q4()
	t4 = time.perf_counter()
	print("Q4 Time: %s\tseconds" % str(t4-t3))


if __name__ == "__main__":
	main()