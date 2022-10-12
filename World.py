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
    
    age : int = 0
    
    # Initialize a world with a specified size.
    # Unsure if the population should also be taken in here or if it should be segregated.
    def __init__(self, width : int, height : int) -> None:
        self.width = width
        self.height = height
        
        self.matrix = np.zeros(shape=(width, height), dtype=int)
    
    def check_cell(self, x : int, y : int) -> int:
        # If a cell is out of bounds, it is treated as occupied.
        # Why? Because it's easier than doing anything else.
        if (x >= self.width or x < 0) or (y >= self.height or y < 0):
            return self.ids['wall']
        
        # Otherwise, return whether or not the cell is actually empty.
        return self.matrix[x, y]
    
    # Check if the cell at a given coordinate is empty.
    def cell_empty(self, x : int, y : int) -> bool:
        return self.check_cell(x, y) == self.ids['empty']
    
    def print_matrix(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                print(self.matrix[x, y], end=' ')
            print()
    
    def kill(self, x_start : int, y_start : int, x_end : int, y_end : int) -> int:
        num_killed : int = 0
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if self.matrix[x, y] == self.ids['agent']:
                    num_killed += 1
                    self.matrix[x, y] = self.ids['empty']
        return num_killed
