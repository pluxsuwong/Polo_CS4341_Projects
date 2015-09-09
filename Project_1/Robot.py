import Node
import math

class Robot: # Baymax
    def __init__(self, curNode):
        self.direction = 'N' # North, East, South, West, North East, North West, South East, South West are represented by N, E, S, W, NE, NW, SE, SW
        self.curNode = curNode # Tuple object, stores the coordinate of the current node
        self.timeTraveled = 0 # The total time the robot has traveled

    # ============================================ Forward ============================================
    # Moves the agent 1 unit forward on the map without changing its facing direction
    # Time required:  the terrain complexity of the square being moved into
    def forward(self, terrain):
        tempNode = terrain.getNode(self.curNode).nextNode(self.direction)
        self.curNode = tempNode.getCoord()
        self.timeTraveled += tempNode.complexity
    

    # ============================================ Bash ============================================
    # Agent charges forward 1 unit without changing its facing direction.
    # After bash action, agent's next action is forward movement of 1 unit for stabilization
    # Time required: 3 (ignores terrain complexity), and the next action taken by the agent must be Forward.
    def bash(self, terrain):
        tempNode1 = terrain.getNode(self.curNode).nextNode(self.direction)
        tempNode2 = tempNode1.nextNode(self.direction)
        self.curNode = tempNode2.getCoord()
        self.timeTraveled += 3 + terrain.getNode(self.curNode[0], self.curNode[1])
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
    
            else:
                print('Robot is not in a valid orientation')
                return
                        
    
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

            else:
                print('Robot is not in a valid orientation')
                return
        
        # If turn parameter is not L or R
        else:
            print('Please enter L or R as parameter')
            return
                        
        
        # Time taken = 1/3 complexity of the node round up
        self.timeTraveled += math.ceil(terrain.getNode(self.curNode[0], self.curNode[1]).complexity/3)
    
    
    
    # ============================================ Demolish ============================================
    # Clear all 8 of the adjacent squares
    # Replaces their terrain complexity with 3
    # Time required:  4
    def demolish(self, terrain):
        
        # Replace the complexity of all the neighboring nodes with 3
        for neighborNode in terrain.getNode(self.curNode[0], self.curNode[1]).allNeighbors:
            terrain.getNode(neighborNode[0], neighborNode[1]).complexity = 3

        # Time taken = 4
        self.timeTraveled += 4

    # ============================================ Get Neighbor with lowest cost ============================================
    def getNeighborWithLowestCost(self):
        for node in












