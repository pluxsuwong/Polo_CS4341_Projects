import fileinput
import re
import sys
import Node
import Terrain


# ========================================= Process Input =========================================
# takes in a filename
# returns a Terrain object
fd = [line for line in fileinput.input(sys.argv[1])]
fileinput.close()
heuristic = int(sys.argv[2])

tempT = []    # 2-D list of lists of nodes
start = (0, 0)
goal = (0, 0)
row = 0

for line in fd:
    raw_row = re.split(r'\t+', line.rstrip('\t\r\n'))
    new_row = []
    col = 0

    for c in raw_row:
        try:
            complexity = int(c)
        except ValueError:
            # is S or G
            if c == 'S':
                start = (col, row)
            elif c == 'G':
                goal = (col, row)
            else:
                print 'Invalid char in input'
            complexity = 1

        new_row.append(Node.Node(col, row, complexity))
        col += 1

    tempT.append(new_row)
    row += 1

# ========================================= A* Search =========================================
# Tri and Peter will work on astar

# Initialize the terrain
terrain = Terrain.Terrain(tempT, start, goal)
terrain.initMovableNeighbors()
terrain.initAllNeighbors()
terrain.initHeuristic(heuristic)

# Initialize the robot
baymax = Robot.Robot(terrain.start)

closedSet = [] # Stores tuple
openSet = [terrain.start] # Stores tuple

while not openSet:
    
    lowestNodeInOpenSet = float("inf")
    for node in openSet:
        if terrain.getNode(node[0], node[1]).f_score < lowestNodeInOpenSet:
            lowestNodeInOpenSet = terrain.getNode(node[0], node[1]).f_score



