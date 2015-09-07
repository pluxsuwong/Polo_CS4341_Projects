import Node
import math

class Robot:
    def __init__(self, direction, curNode, timeTraveled):
        self.direction = direction # North, East, South, West, North East, North West, South East, South West are represented by N, E, S, W, NE, NW, SE, SW
        self.curNode = curNode # The node the robot is currently in
        self.timeTraveled = timeTraveled # The total time the robot has traveled

    # ============================================ Next Node ============================================
    # This function takes in the direction, and returns the neighboring node according to the orientation
    def nextNode(self, nextDir, terrainMap):
        nextCol = -1
        nextRow = -1
        message = 'moving ...'
        
        if nextDir == 'N':
            message = 'Moved North'
            nextCol = self.curNode.col
            nextRow = self.curNode.row - 1
        
        elif nextDir == 'E':
            message = 'Moved East'
            nextCol = self.curNode.col + 1
            nextRow = self.curNode.row
        
        elif nextDir == 'S':
            message = 'Moved South'
            nextCol = self.curNode.col
            nextRow = self.curNode.row + 1

        elif nextDir == 'W':
            message = 'Moved West'
            nextCol = self.curNode.col - 1
            nextRow = self.curNode.row

        elif nextDir == 'NE':
            message = 'Moved North East'
            nextCol = self.curNode.col + 1
            nextRow = self.curNode.row - 1

        elif nextDir == 'NW':
            message = 'Moved North West'
            nextCol = self.curNode.col - 1
            nextRow = self.curNode.row - 1

        elif nextDir == 'SE':
            message = 'Moved South East'
            nextCol = self.curNode.col + 1
            nextRow = self.curNode.row + 1

        elif nextDir == 'SW':
            message = 'Moved South West'
            nextCol = self.curNode.col -1
            nextRow = self.curNode.row + 1
        
        else:
            message = 'Please enter a valid direction'

        # Check the validity of next node:
        if (nextRow > terrainMap.row() - 1) or (nextRow < 0) or (nextCol > terrainMap.col() - 1) or (nextCol < 0):
            print('robot at the edge of map')
            return

        print(message)
        return self.terrainMap[nextCol][nextRow]

    # ============================================ Forward ============================================
    # Moves the agent 1 unit forward on the map without changing its facing direction
    # Time required:  the terrain complexity of the square being moved into
    def forward(self):
        self.curNode = nextNode(self.direction)
        self.timeTraveled += self.curNode.complexity
    

    # ============================================ Bash ============================================
    # Agent charges forward 1 unit without changing its facing direction.
    # After bash action, agent's next action is forward movement of 1 unit for stabilization
    # Time required: 4. 3 for bashing (ignores terrain complexity) and 1 for compulsory forward movement for stabilization
    def bash(self):
        self.curNode = self.curNode.nextNode(self,self.direction)
        self.timeTraveled += 4
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
        self.timeTraveled += math.ceil(self.curNode.complexity/3)
    
    
    
    # ============================================ Demolish ============================================
    # Clear all 8 of the adjacent squares
    # Replaces their terrain complexity with 3
    # Time required:  4
    def demolish(self):
        
        # Replace the complexity of all the neighboring nodes with 3
        for neighborNode in self.curNode.allNeighbors:
            neighborNode.complexity = 3

        # Time taken = 4
        self.timeTraveled += 4













