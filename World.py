import numpy as np

class World():
    width : int = 0
    height : int = 0
    
    # The matrix is going to represent the world in a data format.
    # There is a dictionary that shows what the number in each cell means.
    matrix : np.array(int)
    ids = {
        'empty' : 0,
        'agent' : 1,
        'wall' : 2
    }
    
    # Initialize a world with a specified size.
    # Unsure if the population should also be taken in here or if it should be segregated.
    def __init__(self, width : int, height : int) -> None:
        self.width = width
        self.height = height
        
        self.matrix = np.zeros(shape=(width, height), dtype=int)
    
    # Check if the cell at a given coordinate is empty.
    def cell_empty(self, x : int, y : int) -> bool:
        # If a cell is out of bounds, it is treated as occupied.
        # Why? Because it's easier than doing anything else.
        if (x >= self.width or x < 0) or (y >= self.height or y < 0):
            return False
        
        # Otherwise, return whether or not the cell is actually empty.
        return self.matrix[x, y] == self.ids['empty']
    
    def print_matrix(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                print(self.matrix[x, y], end=' ')
            print()
    
    def kill(self, height: int, width: int) -> None:
        for x in range(height):
            for y in range(width):
                if self.matrix[x,y] == self.ids['agent']:
                    self.matrix[x,y] = self.ids['empty']