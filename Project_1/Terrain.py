class Terrain:
    def __init__(self, terrain, start, goal):
        self.terrain = terrain # 2D list of lists of (initially unlinked) Node objects
        self.start = start # Coordinate tuple
        self.goal = goal # Coordinate tuple

    # Getter for a node in the terrain
    # return a NODE object
    def getNode(self, coordinates):
        return self.terrain[coordinates[0]][coordinates[1]]

    # Informational 2-D map of terrain
    def __repr__(self):
        buf = ""
        for j, line in enumerate(self.terrain):
            for n in line:
                buf += ' ------------------ '
            buf += '\n'
            for i, n in enumerate(line):
                buf += '|'
                if self.start[0] == i and self.start[1] == j:
                    buf += '{:>3}'.format('S')
                elif self.goal[0] == i and self.goal[1] == j:
                    buf += '{:>3}'.format('G')
                else:
                    buf += '{:>3}'.format(str(n.complexity))
                buf += ', ' + '{:>3}'.format(str(n.h_score)) + ', ' + \
                        '{:>3}'.format(str(n.g_score)) + ', ' + \
                        '{:>3}'.format(str(n.f_score)) + '|'
            buf += '\n'
            for n in line:
                buf += ' ------------------ '
            buf += '\n'
                
        return buf

    def initHeuristic(self, heuristic):
        for line in self.terrain:
            for node in line:
                diffX = abs(node.pos[0] - self.goal[0])
                diffY = abs(node.pos[1] - self.goal[1])
        
                if heuristic == 1:
                    node.h_score = 0
    
                elif heuristic == 2:
                    node.h_score = min(diffX, diffY)
    
                elif heuristic == 3:
                    node.h_score = max(diffX, diffY)
        
                elif heuristic == 4:
                    node.h_score = diffX + diffY

                elif heuristic == 5:
                    print 'heuristic 5'

                elif heuristic == 6:
                    print 'heuristic 6'

                else:
                    print 'Invalid numbah'

    # N, E, S, W
    def initMovableNeighbors(self): # TODO: William will take this
        arr = []
        return arr
    
    # N, E, S, W, NE, NW, SE, SW
    def initAllNeighbors(self): # TODO: Jetro
        arr = []
        return arr


