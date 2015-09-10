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

# Move robot to next node
def lowestNode(terrain, openSet):
    if openSet:
        lowestNodeInOS = openSet[0] # arbitrary initial node
        for node in openSet:
            if terrain.getNode(node).f_score < lowestNodeInOS:
                lowestNodeInOS = node
        return lowestNodeInOS
    else:
        print 'The Set is empty'

# Return time cost of moving from curNode to neighbor
def nodeMoveCost(terrain, inDirection, curNode, neighbor)

# Recreates the optimal path
def getMoveSet(terrain, finalNode):
    moveSet = []
    curNode = finalNode
    prevNode = terrain.getNode(curNode).parentNode
    while terrain.start != curNode:
        # Note: parentAction should be stored [action, turn, ...], if at all
        moveSet.extend(curNode.parentActions)
        curNode = terrain.getNode(curNode).parentNode
    return moveSet

# Displays results to screen
def printResults(results):
    print 'Score of Path: ' + str(results[0])
    print 'Number of Actions: ' + str(results[1])
    print 'Number of Nodes Expanded: ' + str(results[2])
    for action in results[3]:
        print action

# ========================================= A* Search =========================================
# Output variables
# Path Score, Num of Actions, Num of Nodes in Closed Set, Actions Taken
results = (0, 0, 0, [])

# Initialize the terrain
terrain = Terrain.Terrain(tempT, start, goal)
terrain.initMovableNeighbors()
terrain.initAllNeighbors()
terrain.initHeuristic(heuristic)

closedSet = [] # List of node tuples already evaluated
openSet = [terrain.start] # List of node tuples to be evaluated
movePath = []
moveSet = []

while not openSet: # while openSet is not empty
    # set current node to the node with the lowest f_score
    curNode = lowestNode(terrain, openSet)

    # check if we're at our goal, or if we've run out of nodes to eval
    if curNode == terrain.goal: # or curNode out of bounds
        moveSet = getMoveSet(terrain, curNode).reverse()
        results[0] = 100 - terrain.getNode(curNode).f_score
        results[1] = len(moveSet)
        results[2] = len(closedSet)
        results[3] = moveSet
        break
    elif not openSet:
        print 'Open set is empty'
        break

    # remove the current node from the open set and place it in the closed set
    openSet.remove(curNode)
    closedSet.append(curNode)

    curNodeNeighbors = terrain.getNode(curNode).movableNeighbors
    # for each neighboring node of the current one
    for neighbor in curNodeNeighbors:
        # if this specific neighbor has already been evaluated
        if closedSet.count(neighbor) > 0:
            continue
        
        # calculate the time cost of moving from the current node to the neighbor
        movCost = nodeMoveCost(terrain, curNode, neighbor) ''''''
        # calculate the potential total g_score 
        gScoreBuf = terrain.getNode(curNode).g_score + movCost ''''''

        # if this specific neighbor is not yet in the open set 
        # or a faster route to the node has been found
        neighborNode = terrain.getNode(neighbor)
        if openSet.count(neighbor) == 0 or gScoreBuf < neighborNode.g_score:
            neighborNode.parentNode = curNode
            neighborNode.g_score = gScoreBuf
            neighborNode.f_score = neighborNode.g_score + neighborNode.h_score
            # add this specific neighbor to the open set if it isn't there
            if openSet.count(neighbor) == 0:
                openSet.append(neighbor)

print terrain
printResults(results)
