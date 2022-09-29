from World import World
import random as r

# Class that represents the individuals populating the world.
class LittleGuy():
    # Position in the world that this individual occupies.
    _x : int = -1
    _y : int = -1
    # The world that this individual lives in.
    _world : World
    
    # Forward vector; the last direction that this individual moved in.
    _forward : tuple[int, int] = (0, 0)
    
    def __init__(self, world : World) -> None:
        self._world = world
    
    def place_radomly(self) -> None:
        # Randomly distribute this individual within the world.
        # Start with a set of coordinates that are out of bounds.
        x : int = -1
        y : int = -1
        # I wish python had do-while loops.
        while (x < 0 or y < 0) or (not self._world.cell_empty(x, y)):
            # Choose a coordinate pair inside the world, making sure the cell is not occupied by anything.
            # The range of randint() is closed on both ends, hence the -1.
            x = r.randint(0, self._world.width - 1)
            y = r.randint(0, self._world.height - 1)
        # Set the individual to that coordinate and update the matrix accordingly.
        self.set_coordinates(x, y)
        self._world.matrix[x, y] = self._world.ids['agent']
    
    # Move this individual to a specific place in the world.
    def set_coordinates(self, x : int, y : int) -> bool:
        # Check if the target cell is unoccupied.
        # If there is already something there, then stop.
        if not self._world.cell_empty(x, y):
            return False
        
        # When moving, make sure to empty the space this agent was previously in.
        # The >= 0 check is because positions are initialized to (-1, -1) and we don't want to change anything
        # if this individual is being given a position for the first time or if the coordinates are out of bounds.
        if self._x >= 0 and self._y >= 0:
            self._world.matrix[self._x, self._y] = self._world.ids['empty']
        
            # Update the forward vector.
            self._forward = (x - self._x, y - self._y)
        
        # Move to the new location.
        self._x = x
        self._y = y
        self._world.matrix[self._x, self._y] = self._world.ids['agent']
        
        return True
    
    # All the movement functions we could ever need.
    def move_left(self) -> bool:
        return self.set_coordinates(self._x - 1, self._y)
    def move_right(self) -> bool:
        return self.set_coordinates(self._x + 1, self._y)
    def move_up(self) -> bool:
        return self.set_coordinates(self._x, self._y - 1)
    def move_down(self) -> bool:
        return self.set_coordinates(self._x, self._y + 1)
    def move_up_left(self) -> bool:
        return self.set_coordinates(self._x - 1, self._y - 1)
    def move_up_right(self) -> bool:
        return self.set_coordinates(self._x + 1, self._y - 1)
    def move_down_left(self) -> bool:
        return self.set_coordinates(self._x - 1, self._y + 1)
    def move_down_right(self) -> bool:
        return self.set_coordinates(self._x + 1, self._y + 1)
    def move_forward(self) -> bool:
        return self.set_coordinates(self._x + self._forward[0], self._y + self._forward[1])
    def move_random(self) -> bool:
        move = r.choice([self.move_left, self.move_right, self.move_up, self.move_down,
                         self.move_up_left, self.move_up_right, self.move_down_left, self.move_down,
                         self.move_forward])
        return move()