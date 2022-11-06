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
    def matrix_to_str(self) -> str:
        string : str = ''
        for y in range(self.height):
            for x in range(self.width):
                string += str(self.matrix[x, y])
            if y != self.height - 1:
                string += ' '
        return string
    
    def kill(self, population, x_start : int, y_start : int, x_end : int, y_end : int) -> int:
        num_killed : int = 0
        for x in range(x_start, x_end):
            for y in range(y_start, y_end):
                if self.matrix[x, y] == self.ids['agent']:
                    # increase the number of killed
                    num_killed += 1
                    # find the guy at this location in the population
                    # there is probably a better way to do this, but this is the first way that I though of
                    guy = [guy for guy in population if guy._x == x and guy._y == y][0]
                    # remove the guy
                    population.remove(guy)
                    # set the spot in the world to be empty
                    self.matrix[x, y] = self.ids['empty']
        return num_killed
