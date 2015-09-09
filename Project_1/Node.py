import Robot
import Terrain

# This class represent a single node

class Node:
    def __init__(self, col, row, complexity):
        self.pos = (col, row)
        self.complexity = complexity
        self.h_score = float("inf")
        self.g_score = float("inf")
        self.f_score = float("inf")
        self.parentNode = None # The node (tuple) that this node came from
        self.allNeighbors = [] # List of all neighbors (tuples) of this node: N, E, S, W, NE, NW, SE, SW
        self.movableNeighbor = [] # List of 4 neighbors (tuples) that the robot can move to: N, E, S, W

    # This function takes in the direction, and returns the tuple according to the orientation
    def nextNode(self, direction):
        
        if direction == 'N':
	    #returns the node to the north of the current node (12'oclock)
            #access the map
            return self.movableNeighbor[0]

        elif direction == 'E':
            #returns the node to the east of the current node (3'oclock)
            return self.movableNeighbor[1]

        elif direction == 'S':
            #returns the node to the south of the current node (6'oclock)
            return self.movableNeighbor[2]

        elif direction == 'W':
            #returns the node to the west of the current node (9'oclock)
            return self.movableNeighbor[3]

        else: 
            #any other cases
            print 'invalid direction'

