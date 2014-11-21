#! /usr/bin/python

import Graph
import copy
from heapq import *
import sys
import time


filename = "placeholder"
cutoff = 100000.0


class TSPNode:
    
    
    def __init__(self, aGraph, aPath=[], pathLength=0):
        self.state = aGraph
        self.path = copy.copy(aPath)
        self.pathLength = pathLength
        self.bound = self.computeBound()


    def addVertex(self, vertex):
        if len(self.path):
            self.pathLength += self.state.get_dist(self.path[-1],vertex)
        else:
            self.pathLength = 0
        self.path.append(vertex)
        self.bound = self.computeBound()
    def __lt__(self, otherNode):
        return self.bound < otherNode.bound
    def __le__(self, otherNode):
        return self.bound <= otherNode.bound
    def __gt__(self, otherNode):
        return self.bound > otherNode.bound
    def __ge__(self, otherNode):
        return self.bound >= otherNode.bound

    def computeBound(self):
	    shortest = 0
	    for name1 in self.state.nodeNames:
		short = -1
		if name1 not in self.path:
		    for name2 in self.state.nodeNames:
		        if name2 not in self.path and name1 != name2:
		            if short == -1 or self.state.get_dist(name1, name2) < short:
		                short = self.state.get_dist(name1, name2)
		if short:
		    shortest += short
	    return (shortest + self.pathLength)	
	    	    



def travelingSalesperson(aGraph):
   
    visitedNodes = 0 # to keep track of how many nodes we 'visit'
    optimalTour = None # Until we discover the first tour

   
    priorityQueue = []

    
    currentNode = TSPNode(aGraph)

    
    currentNode.addVertex(aGraph.get_names()[0])

    
    heappush(priorityQueue, currentNode)

    
    while (len(priorityQueue) > 0):
	currentTime = time.clock()	
	if((currentTime - startTime) <= cutoff):
		
		currentNode = heappop(priorityQueue)

		
		if not optimalTour or (currentNode.bound < optimalTour.pathLength):
		    visitedNodes += 1
		    
		    if len(currentNode.path) == aGraph.size():
		        if aGraph.get_dist(currentNode.path[-1], currentNode.path[0]) != None:
		            currentNode.addVertex(currentNode.path[0])
		            if not optimalTour or \
		                  (currentNode.pathLength < optimalTour.pathLength):
		                optimalTour = currentNode
				endTime = time.clock()
				f=open(filename+".trace",'a')
				f.write(str(endTime-startTime)+" "+str(optimalTour.pathLength)+"\n")
			
		    else:
		        for node in aGraph.get_names():
		            if node not in currentNode.path and \
		                  aGraph.get_dist(currentNode.path[-1], node) != None:
		                newNode = TSPNode(currentNode.state, 
		                                  currentNode.path, 
		                                  currentNode.pathLength)
		                newNode.addVertex(node)
		                if not optimalTour or \
		                      (newNode.bound < optimalTour.pathLength):
		                    heappush(priorityQueue, newNode)

		else:  
			return (visitedNodes, optimalTour)
	else:
		sys.exit(0)

    return (visitedNodes, optimalTour)



if __name__ == '__main__':
    filename = sys.argv[1]
    cutoff = float(sys.argv[2])
    print cutoff
    f=open(filename+".trace",'w')
    f.close()
    aGraph = Graph.fromTSPFile(filename)
    print aGraph
    startTime = time.clock()
    (visited, solution) = travelingSalesperson(aGraph)
    print 'Visited ', visited, ' nodes'
    if solution:
	f=open(filename+".sol",'w')
	f.write(str(solution.pathLength)+"\n")
	for vertex in range(0,len(solution.path)):
		f.write(str(solution.path[vertex])+",")
	f.close()
        print 'Shortest tour is ',solution.pathLength, ' long:'
        print solution.path
    else:
        print 'No tour found'
