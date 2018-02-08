#!/usr/bin/env python
from ArcReader import ArcReader
import sys
import time

def q1():
	pass

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
	q1()
	t1 = time.perf_counter()
	print("Q1 Time: %s\tseconds" % str(t1-t0))
	
	## Question 2
	t1 = time.perf_counter()
	q2()
	t2 = time.perf_counter()
	print("Q2 Time: %s\tseconds" % str(t2-t1))
	
	## Question 3
	t2 = time.perf_counter()
	q3()
	t3 = time.perf_counter()
	print("Q3 Time: %s\tseconds" % str(t3-t2))
	
	## Question 4
	t3 = time.perf_counter()
	q4()
	t4 = time.perf_counter()
	print("Q4 Time: %s\tseconds" % str(t4-t3))


if __name__ == "__main__":
	main()