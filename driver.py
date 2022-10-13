from World import World
from LittleGuy import LittleGuy
from Brain import *
import numpy as np

world : World = World(width=8, height=8)
population : list[LittleGuy] = []
#for _ in range(4):
#    population.append(LittleGuy(world))
#for p in population:
#    p.place_radomly()

#world.print_matrix()

#for _ in range(100):
#    print()
#    for x in population:
#        x.move_random()
#    world.print_matrix()

##killed : int = world.kill(0, 0, world.width // 2, world.height)
#killed : int = world.kill(1, 1, world.width - 1, world.height - 1)
#print()
#world.print_matrix()
#print(f"killed {killed} little guys")




john : LittleGuy = LittleGuy(world)
john.brain = Network(
    [
        Node(type=0, transformation_function=john.check_forward), #0
        Node(2, lambda x: 1 if x == 0 else -1), #1
        Node(1, john.move_forward), #2
        Node(1, john.move_random), #3
        Node(0, john.check_time), #4
        Node(2, lambda x: 2 / np.exp(((x - 4) / 2)**2) if x < 5 else 0), #5
        Node(0, john.rand) #6
    ],
    [
        Connection(input=0, output=1, weight=1), 
        Connection(1, 2, 1), 
        Connection(1, 3, -1),
        Connection(4, 5, 1),
        Connection(5, 3, 1.5),
        Connection(6, 5, 0.8)
    ]
)
john.place_randomly()

for t in range(10):
    world.age = t
    print()
    
    f = john.brain.evaluate()
    print(f)
    f()
    
    world.print_matrix()