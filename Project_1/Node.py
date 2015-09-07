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
        self.parentNode = parentNode
        self.neighbors = neighbors

    # This function takes in the direction, and returns the node according to the orientation
    def nextNode(self, dir):
        print("Hello")

