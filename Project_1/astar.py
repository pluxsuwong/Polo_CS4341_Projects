import fileinput
import re
import Node
import Terrain

# N, E, S, W
def initMovableNeighbor(col, row): # TODO: need to know map dimensions
    arr = []
    return arr

# N, E, S, W, NE, NW, SE, SW
def initAllNeighbors(movableNeighbor, col, row): # TODO: need to know map dimensions
    arr = []
    return arr

fd = [line for line in fileinput.input()]

terrain = []    # 2-D list of lists of nodes
start = [0, 0]
goal = [0, 0]
row = 0

for line in fd:
    raw_row = re.split(r'\t+', line.rstrip('\t\r\n'))
    new_row = []
    col = 0

    for c in raw_row:
        h_score = float("inf")
        g_score = float("inf")
        f_score = float("inf")
        parentNode = None
        movableNeighbor = initMovableNeighbor(col, row)
        allNeighbors = initAllNeighbors(movableNeighbor, col, row)
        
        try:
            complexity = int(c)
        except ValueError:
            # is S or G
            if c == 'S':
                start = [col, row]
            elif c == 'G':
                goal = [col, row]
            else:
                print 'Invalid char in input'
            complexity = 1

        new_row.append(Node.Node(
            row, col, complexity,
            h_score, g_score, f_score,
            parentNode, allNeighbors, movableNeighbor))
        col += 1

    terrain.append(new_row)
    row += 1



print terrain
