from World import World
from Brain import *
import random as r
import behaviors

# Class that represents the individuals populating the world.
class LittleGuy():
    # Position in the world that this individual occupies.
    _x : int = -1
    _y : int = -1
    # The world that this individual lives in.
    _world : World
    
    brain : Network = None
    
    # Forward vector; the last direction that this individual moved in.
    _forward : tuple[int, int] = (0, 0)
    
    _A : float = 1
    _B : float = 1
    _C : float = 1
    _D : float = 1
    
    def __init__(self, world : World) -> None:
        self._world = world
        self.brain = None
    
    def place_randomly(self) -> None:
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
        
        self._forward = (r.choice([-1, 0, 1]), r.choice([-1, 0, 1]))
        if self._forward == (0, 0):
            if r.choice([0, 1]) == 0:
                self._forward = (self._forward[0], r.choice([-1, 1]))
            else:
                self._forward = (r.choice([-1, 1]), self._forward[1])
    
    # Move this individual to a specific place in the world.
    def set_coordinates(self, x : int, y : int) -> bool:
        # Don't move to any out of bounds cells.
        if x >= self._world.width or x < 0 or y >= self._world.height or y < 0:
            return False
        
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
    
    def randomize(self):
        self.place_randomly()		
  
        self._A = 10 * (2 * r.random() - 1)
        self._B = 10 * (2 * r.random() - 1)
        self._C = 10 * (2 * r.random() - 1)
        self._D = 10 * (2 * r.random() - 1)
        
        for _ in range(self.brain.MAX_INTERNAL_NEURONS):
            if r.random() <= 0.1:
                self.brain.nodes.append(
                    Node(
                        type=2,
                        transformation_function=r.choice([
                            behaviors.sigmoid,
                            behaviors.step,
                            behaviors.abs,
                            behaviors.piece,
                            behaviors.parabola
                        ])
                    )
                )
        for _ in range(self.brain.MAX_CONNECTIONS):
            if r.random() <= 0.1:
                self.brain.connections.append(
                    Connection(
                        input=r.choice(range(len(self.brain.nodes))), 
                        output=r.choice(range(len(self.brain.nodes))),
                        weight=10 * (2 * r.random() - 1)
                    )
                )