import fileinput
import re
import sys
import math
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

# Return lowest complexity node in open set
def lowestNode(terrain, openSet):
    if openSet:
        lowestNodeInOS = openSet[0] # arbitrary initial node
        for node in openSet:
            if terrain.getNode(node).f_score < terrain.getNode(lowestNodeInOS).f_score:
                lowestNodeInOS = node
                # print 'Replaced lowest node!'
            # print "BUG: " + str(node) + ' had ' + str(terrain.getNode(node).f_score)
        # print 'Checkpoint 2: ' + str(lowestNodeInOS) + " " + str(terrain.getNode(lowestNodeInOS).f_score)
        return lowestNodeInOS
    else:
        print 'The Set is empty'

# Dictionary for bearings
dirDict = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
enumDirDict = {0: 'N', 1: 'E', 2: 'S', 3: 'W'}

# Return time cost of moving to neighbor from curNode
# Note: Really ghetto function
def nodeMoveCost(terrain, curNode, neighbor):
    # store current node object in variable
    cNode = terrain.getNode(curNode)
    # translate c->n node direction to number
    movDirIndex = cNode.movableNeighbors.index(neighbor)
    # initial direction into node
    curDir = dirDict[cNode.robotBearing]
    # find number of necessary turns
    rawTurns = movDirIndex - curDir
    turns = 0
    if rawTurns == 3:
        turns = -1
    elif rawTurns == -3:
        turns = 1
    else:
        turns = rawTurns

    numTurns = abs(turns)
    # store neighbor node object in variable
    nNode = terrain.getNode(neighbor)
    # cost for 1 turn
    cost_t = math.ceil(float(cNode.complexity)/3)
    # total cost for turns+fwd to get to neighbor
    cost_a = cost_t*numTurns + nNode.complexity
    # total cost for turns+bash to get to neighbor
    cost_b = cost_t*numTurns + 3
    # actions taken by parent to get to child buffer
    actions = []
    # store orientation
    direction = enumDirDict[movDirIndex]
    
    if cNode.parentActions.count('B') > 0:
        if numTurns == 0:
            actions.append('F')
            return (cost_a, actions, direction)
        else:
            return None
    else:
        # add turns to 
        for i in range(0, numTurns):
            # store directions taken by parent to reach child
            if turns < 0:
                actions.append('L')
            else:
                actions.append('R')
    
    # DEBUG
    # print terrain.getNode(curNode)

    try:
        nnNode = terrain.getNode(nNode.movableNeighbors[movDirIndex])
        # B+F is heuristically good and is cheaper than F+F
        if nNode.h_score > nnNode.h_score and nNode.complexity > 3:
            actions.append('B')
            return (cost_b, actions, direction)
        else:
            actions.append('F')
            return (cost_a, actions, direction)
    except TypeError:
        actions.append('F')
        return (cost_a, actions, direction)

# Recreates the optimal path
def getMoveSet(terrain, finalNode):
    moveSet = []
    curNode = finalNode
    # print 'Recounting Path...'
    while terrain.start != curNode:
        # Note: action should be stored [action, turn, ...], if at all
        moveSet.extend(list(reversed(terrain.getNode(curNode).parentActions)))
        curNode = terrain.getNode(curNode).parentNode
        # print terrain.getNode(curNode)
    return moveSet

# Displays results to screen
def printResults(results):
    print 'Score of Path: ' + str(results[0])
    print 'Number of Actions: ' + str(results[1])
    print 'Number of Nodes Expanded: ' + str(results[2])
    print 'F: Forward, B: Bash, L: Turn Left, R: Turn Right'
    for action in results[3]:
        print action

# ========================================= A* Search =========================================
# Output variables
# Path Score, Num of Actions, Num of Nodes in Closed Set, Actions Taken
results = [0, 0, 0, []]
# Initialize the terrain
terrain = Terrain.Terrain(tempT, start, goal)
terrain.initMovableNeighbors()
terrain.initAllNeighbors()
terrain.initHeuristic(heuristic)
startNode = terrain.getNode(start)
startNode.robotBearing = 'N'
startNode.g_score = float(0)
startNode.f_score = float(startNode.g_score + startNode.h_score)
terrain.setNode(start, startNode)

closedSet = [] # List of node tuples already evaluated
openSet = [terrain.start] # List of node tuples to be evaluated
movePath = []
moveSet = []

while openSet: # while openSet is not empty
    # set current node to the node with the lowest f_score
    curNode = lowestNode(terrain, openSet)
    # print 'Checkpoint 0: curNode = ' + str(curNode)
    # print '              openSet = ' + str(openSet)
    # print '              closedSet = ' + str(closedSet)

    # check if we're at our goal, or if we've run out of nodes to eval
    if curNode == terrain.goal: # or curNode out of bounds
        # add last move to final node
        moveSet = list(reversed(getMoveSet(terrain, curNode)))
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
    # print 'Checkpoint 1: curNodeNeighbors = ' + str(curNodeNeighbors)
    # for each neighboring node of the current one
    for neighbor in curNodeNeighbors:
        movCost = None
        # if this specific neighbor has already been evaluated
        if closedSet.count(neighbor) > 0 or neighbor is None:
            # print 'DEBUG: ' + str(neighbor) + ' was skipped'
            continue
        
        movCost = nodeMoveCost(terrain, curNode, neighbor)
        
        # else:
        #     print 'DEBUG: ' + str(neighbor) + ' wasn\'t skipped'
        
        # calculate the time cost of moving from the current node to the neighbor
        # tuple of (cost, [actions, ...])
        
        # calculate the potential total g_score 
        try:
            gScoreBuf = terrain.getNode(curNode).g_score 
            if gScoreBuf == float("inf"):
                gScoreBuf = movCost[0]
            else:
                gScoreBuf += movCost[0]
        except TypeError:
            continue

        # if this specific neighbor is not yet in the open set 
        # or a faster route to the node has been found
        neighborNode = terrain.getNode(neighbor)
        if openSet.count(neighbor) == 0 or gScoreBuf < neighborNode.g_score:
            neighborNode.parentNode = curNode
            neighborNode.parentActions = movCost[1]
            neighborNode.robotBearing = movCost[2]
            neighborNode.g_score = gScoreBuf
            neighborNode.f_score = neighborNode.g_score + neighborNode.h_score
            # add this specific neighbor to the open set if it isn't there
            if openSet.count(neighbor) == 0:
                openSet.append(neighbor)
            terrain.setNode(neighborNode.pos, neighborNode)

print terrain
printResults(results)

