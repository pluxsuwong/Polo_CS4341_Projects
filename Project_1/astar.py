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

# ========================================= Helper Functions =========================================

# Returns a tuple representing a node
def getLowestNode(terrain, openSet):
    if openSet:
        lowestNode = openSet[0]
        for node in openSet:
            if terrain.getNode(node).f_score < lowestNode:
                lowestNode = node
        return lowestNode
    else:
        print 'The Set is empty'

# Displays results to screen
def printResults(results):
    print 'Score of Path: ' + str(results[0])
    print 'Number of Actions: ' + str(results[1])
    print 'Number of Nodes Expanded: ' + str(results[2])
    for action in results[3]:
        print action

# ========================================= A* Search =========================================
# Tri and Peter will work on astar
# Output variables
# Path Score, Num of Actions, Num of Nodes in Closed List, Actions Taken
results = (0, 0, 0, [])

# Initialize the terrain
terrain = Terrain.Terrain(tempT, start, goal)
terrain.initMovableNeighbors()
terrain.initAllNeighbors()
terrain.initHeuristic(heuristic)

# Initialize the robot
baymax = Robot.Robot(terrain.start)

closedSet = [] # List of node tuples already evaluated
openSet = [terrain.start] # List of node tuples to be evaluated
moveSet = []

while not openSet: # while openSet is not empty
    baymax.curNode = getLowestNode(terrain, openSet) # get the node with the lowest f score in the openSet
    if baymax.curNode == terrain.goal:
        results[0] = 100 - baymax.timeTraveled
        results[1] = len(moveSet)
        results[2] = len(closedSet)
        results[3] = moveSet
        break

    openSet.remove(baymax.curNode)
    closedSet.append(baymax.curNode)
    curNode = terrain.getNode(baymax.curNode)
    for node in baymax.curNode:
        # ...

# printResults(results)
