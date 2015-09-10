class Terrain:
    def __init__(self, terrain, start, goal):
        self.terrain = terrain # 2D list of lists of (initially unlinked) Node objects
        self.start = start # Coordinate tuple
        self.goal = goal # Coordinate tuple

    # Getter for a node in the terrain
    # return a NODE object
    def getNode(self, coordinates):
        return self.terrain[coordinates[0]][coordinates[1]]

    # Setter for a node in the terrain
    # set a NODE object
    def setNode(self, coordinates, aNodeObj):
        self.terrain[coordinates[0]][coordinates[1]] = aNodeObj

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
    def initMovableNeighbors(self):

        terrainRows = len(self.terrain)
        terrainCols = len(self.terrain[0])
        
        for line in self.terrain:
            for node in line:
                northNeighbor = (node.pos.col, node.pos.row-1)
                eastNeighbor = (node.pos.col+1, node.pos.row)
                southNeighbor = (node.pos.col, node.pos.row+1)
                westNeighbor = (node.pos.col-1, node.pos.row)

                # logic for setting None neighbors if out of bounds

                if (node.pos.row < 1):
                    northNeighbor = None

                if (node.pos.col >= terrainCols):
                    eastNeighbor = None

                if (node.pos.row >= terrainRows):
                    southNeighbor = None

                if (node.pos.col < 1):
                    westNeighbor = None
                    
                
            node.movableNeighbors = [northNeighbor,eastNeighbor,southNeighbor,westNeighbor]    
    
    # N, E, S, W, NE, NW, SE, SW
    def initAllNeighbors(self):

        terrainRows = len(self.terrain)
        terrainCols = len(self.terrain[0])
        
        for line in self.terrain:
            for node in line:
                northNeighbor = (node.pos.col, node.pos.row-1)
                eastNeighbor = (node.pos.col+1, node.pos.row)
                southNeighbor = (node.pos.col, node.pos.row+1)
                westNeighbor = (node.pos.col-1, node.pos.row)
                northEastNeighbor = (node.pos.col+1, node.pos.row-1)
                southEastNeighbor = (node.pos.col+1, node.pos.row+1)
                southWestNeighbor = (node.pos.col-1, node.pos.row+1)
                northWestNeighbor = (node.pos.col-1, node.pos.row-1)

                # logic for setting None neighbors if out of bounds

                if (node.pos.row < 1):
                    northNeighbor = None
                    northWestNeighbor = None
                    northEastNeighbor = None

                if (node.pos.col >= terrainCols):
                    eastNeighbor = None
                    northEastNeighbor = None
                    southEastNeighbor = None

                if (node.pos.row >= terrainRows):
                    southNeighbor = None
                    southEastNeighbor = None
                    southWestNeighbor = None

                if (node.pos.col < 1):
                    westNeighbor = None
                    northWestNeighbor = None
                    southWestNeighbor = None
                
            node.allNeighbors = [northNeighbor,eastNeighbor,southNeighbor,westNeighbor,northEastNeighbor,southhEastNeighbor,southWestNeighbor,northWestNeighbor]         


