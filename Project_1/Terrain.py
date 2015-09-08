class Terrain:
    def __init__(self, terrain, start, goal):
        self.terrain = terrain # 2D list of lists of (initially unlinked) Node objects
        self.start = start # Coordinate tuple
        self.goal = goal # Coordinate tuple
    

    # Getter for a node in the terrain
    # return a NODE object
    def getNode(self, col, row):
        return self.terrain[col][row]

    # N, E, S, W
    def initMovableNeighbors(self): # TODO: need to know map dimensions
        arr = []
        return arr
    
    # N, E, S, W, NE, NW, SE, SW
    def initAllNeighbors(self, col, row): # TODO: need to know map dimensions
        arr = []
        return arr









