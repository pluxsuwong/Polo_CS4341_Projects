class Terrain:
    def __init__(self, terrain, start, goal):
        self.terrain = terrain # 2D list of lists of (initially unlinked) Node objects
        self.start = start # Coordinate tuple
        self.goal = goal # Coordinate tuple

    # Getter for a node in the terrain
    # return a NODE object
    def getNode(self, col, row):
        return self.terrain[col][row]

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

    # N, E, S, W
    def initMovableNeighbors(self): # TODO: William will take this
        arr = []
        return arr
    
    # N, E, S, W, NE, NW, SE, SW
    def initAllNeighbors(self): # TODO: Jetro
        arr = []
        return arr









