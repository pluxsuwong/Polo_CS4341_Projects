import Node
import math

class Robot:
    def __init__(self, direction, curNode, timeTraveled, terrain):
        self.terrain = terrain # The robot needs to now the whole map
        self.direction = direction # North, East, South, West, North East, North West, South East, South West are represented by N, E, S, W, NE, NW, SE, SW
        self.curNode = curNode # The node the robot is currently in
        self.timeTraveled = timeTraveled # The total time the robot has traveled

    # ============================================ Next Node ============================================
    # This function takes in the direction, and returns the neighboring node according to the orientation
    def nextNode(self, dir):
        if dir == 'N':
            return self.terrain[self.curNode.col][self.curNode.row - 1]
        
        elif dir == 'E':
            return self.terrain[self.curNode.col + 1][self.curNode.row]
        
        elif dir == 'S':
            return self.terrain[self.curNode.col][self.curNode.row + 1]

        elif dir == 'W':
            return self.terrain[self.curNode.col - 1][self.curNode.row]

        elif dir == 'NE':
            return self.terrain[self.curNode.col + 1][self.curNode.row - 1]

        elif dir == 'NW':
            return self.terrain[self.curNode.col - 1][self.curNode.row - 1]

        elif dir == 'SE':
            return self.terrain[self.curNode.col + 1][self.curNode.row + 1]

        elif dir == 'SW':
            return self.terrain[self.curNode.col -1 ][self.curNode.row + 1]



    # ============================================ Forward ============================================
    # Moves the agent 1 unit forward on the map without changing its facing direction
    # Time required:  the terrain complexity of the square being moved into
    def forward(self):
        self.curNode = nextNode(self.direction)
        self.timeTraveled += self.curNode.complexity
    

    # ============================================ Bash ============================================
    def bash(self):
        print('bash')
    
    
    # ============================================ Turn ============================================
    # Turn the agent 90 degree either left or right.
    # Time required:  1/3 of the numeric value of the square currently occupied (rounded up).
    def turn(self, leftOrRight):
        
        # If turn left
        if leftOrRight == 'L':
            
            if self.direction == 'N':
                self.direction = 'W'
            
            elif self.direction == 'E':
                self.direction == 'N'
            
            elif self.direction == 'S':
                self.direction = 'E'
            
            elif self.direction == 'W':
                self.direction = 'S'
    
        # If turn right
        elif leftOrRight == 'R':
            if self.direction == 'N':
                self.direction = 'E'
            
            elif self.direction == 'E':
                self.direction = 'S'
            
            elif self.direction == 'S':
                self.direction = 'W'
            
            elif self.direction == 'W':
                self.direction = 'N'
        
        # Time taken = 1/3 complexity of the node round up
        self.timeTraveled += math.ceil(self.curNode.complexity/3)
    
    
    
    # ============================================ Demolish ============================================
    # Clear all 8 of the adjacent squares
    # Replaces their terrain complexity with 3
    # Time required:  4
    def demolish(self):
        
        # Replace the complexity of all the neighboring nodes with 3
        for neighborNode in self.curNode.neighbors:
            neighborNode.complexity = 3

        # Time taken = 4
        self.timeTraveled += 4











