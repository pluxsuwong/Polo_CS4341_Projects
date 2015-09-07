import Robot
import Terrain

# This class represent a single node

class Node:
    def __init__(self, row, col, complexity, h_score, g_score, f_score, parentNode, neighbors):
        self.row = row
        self.col = col
        self.complexity = complexity
        self.h_score = h_score
        self.g_score = g_score
        self.f_score = f_score
        self.parentNode = parentNode # The node that this node came from
        self.neighbors = neighbors # The neighbors of the this node contains: N, E, S, W, NE, NW, SE, SW


