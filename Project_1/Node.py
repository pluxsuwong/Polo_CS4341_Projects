import Robot
import Terrain

# This class represent a single node

class Node:
    def __init__(self, row, col, complexity, h_score, g_score, f_score, parentNode, allNeighbors, movableNeighbor):
        self.row = row
        self.col = col
        self.complexity = complexity
        self.h_score = h_score
        self.g_score = g_score
        self.f_score = f_score
        self.parentNode = parentNode # The node that this node came from
        self.allNeighbors = allNeighbors # All neighbors of the this node contains: N, E, S, W, NE, NW, SE, SW
        self.movableNeighbor = movableNeighbor # The 4 neighbors that the robot can move to: N, E, S, W

    # This function takes in the direction, and returns the node according to the orientation
    def nextNode(self, direction):
        if direction == 'N':
	    #returns the node to the north of the current node (12'oclock)
            #access the map 
            self.row = row + 1
            return movableNeighbor[0]

        elif direction == 'E':
            #returns the node to the east of the current node (3'oclock)
            self.col = col + 1
            return movableNeighbor[1]

        elif direction == 'S':
            #returns the node to the south of the current node (6'oclock)
            self.row = row - 1
            return movableNeighbor[2]

        elif direction == 'W':
            #returns the node to the west of the current node (9'oclock)
            self.col = col - 1
            return movableNeighbor[3]

        else: 
            #any other cases
            print 'invalid direction'



