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


