#!/usr/bin/python

import string
import random
from randomIntList import randomIntList
import math

PI = 3.141592
CONVERT = 6378.388

class Graph:
    def __init__(self, nodeNames,coord_type):
       
        self.coord_type = coord_type
        self.nodeNames = nodeNames
        self.matrix = [None]* len(nodeNames)
        self.cache = {}

    def get_names(self):
        return self.nodeNames


    def index(self, nodeName):
        return self.nodeNames.index(nodeName)


    def size(self):
        return len(self.matrix)

    def length(self):
        return len(self.nodeNames)


    def set_coordinates(self, node, coordinates):
        if(self.coord_type=='GEO'):
            (x,y)= coordinates
            deg = math.floor(x)
            min = x- deg
            rad1 = PI * (deg + 5.0 * min/ 3.0) / 180.0
            deg = math.floor(y)
            min = y- deg
            rad2 = PI * (deg + 5.0 * min/ 3.0) / 180.0
            self.matrix[self.nodeNames.index(node)] = (rad1,rad2)

        else:
            self.matrix[self.nodeNames.index(node)] = coordinates


    def get_dist(self, fromNode, toNode):
        if self.coord_type=='EUC_2D':
           if not (self.cache.has_key((fromNode, toNode)) or \
                 (self.cache.has_key((toNode, fromNode)))):
              (x1, y1) = self.matrix[self.nodeNames.index(fromNode)]
              (x2, y2) = self.matrix[self.nodeNames.index(toNode)]
              self.cache[(fromNode,toNode)] = math.sqrt((x1-x2)**2 + (y1-y2)**2)

         

        else:
            (x1, y1) = self.matrix[self.nodeNames.index(fromNode)]
            (x2, y2) = self.matrix[self.nodeNames.index(toNode)]
            q1 = math.cos( y1 - y2 )
            q2 = math.cos( x1 - x2 )
            q3 = math.cos( x1 + x2 )
            dij = int(( CONVERT * math.acos( 0.5*((1.0+q1)*q2 - (1.0-q1)*q3) ) + 1.0))
            self.cache[(fromNode,toNode)] = dij
            
            
	if self.cache.has_key((fromNode, toNode)):
              return self.cache[(fromNode, toNode)]
        else:
              return self.cache[(toNode, fromNode)]


    def __str__(self):
        _FMT = '%10.10s'

       
        result = _FMT % ' '

       
        for name in self.nodeNames:
            result += _FMT % name
        result += '\n'

       
        i = 0
        for nodeList in self.matrix:
            # Node name
            result += _FMT % self.nodeNames[i]
            i += 1
            # List of integer values
            for node in nodeList:
                result += _FMT % node
            result += '\n'

        return result



def fromTSPFile(Filename):
    File = open(Filename)

    params = {}
    line = File.readline()
    while line.find(':') >= 0:
        (key, value) = line.split(':')
        params[string.strip(key)] = string.strip(value)   #strip removes whitespaces
        line = File.readline()


    if params['EDGE_WEIGHT_TYPE'] not in ['EUC_2D', 'GEO']:
        raise NotImplementedError('Unsupported format %s' % params['EDGE_WEIGHT_TYPE'])

    elif params['EDGE_WEIGHT_TYPE'] in ['EUC_2D','GEO']:
        input_graph = Graph(range(int(params['DIMENSION'])),params['EDGE_WEIGHT_TYPE'] )
      
        for i in range(input_graph.size()):
            (num, x, y) = File.readline().split()
            input_graph.set_coordinates(i, (float(x), float(y)))

    else:
	raise NotImplementedError('%s not supported' % params['EDGE_WEIGHT_TYPE'])

    File.close()

    return input_graph




