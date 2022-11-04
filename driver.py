from LittleGuy import LittleGuy
from World import World
from behaviors import *
from Brain import *
import random as r
import copy

def repopulate(current_pop : list[LittleGuy]) -> list[LittleGuy]:
    population : list[LittleGuy] = []
    while len(population) < pop_size:
        # Randomly choose 2 parents.
        p1 = r.choice(current_pop)
        p2 = r.choice(current_pop)
        
        child = LittleGuy(world)
        child.place_randomly()
        population.append(child)
        
        # Randomly choose attributes from each parent.
        # Inherit brain structure from p1.      
        child.brain = copy.deepcopy(p1.brain)
        # Inherit other properties from p2.
        child._A = p2._A
        child._B = p2._B
        child._C = p2._C
        child._D = p2._D
        
        # Mutate the child after inheriting.
        child.brain.mutate()
    
    return population

STOCK_BRAIN = Network(
    nodes=[
        # input neurons
        Node(0, pos_x),
        Node(0, pos_y),
        Node(0, rand),
        Node(0, check_time),
        Node(0, check_forward),
        Node(0, oscillator),
        # output neurons
        Node(1, move_left),
        Node(1, move_right),
        Node(1, move_up),
        Node(1, move_down),
        Node(1, move_up_left),
        Node(1, move_up_right),
        Node(1, move_down_left),
        Node(1, move_down_right),
        Node(1, move_forward),
        Node(1, move_reverse),
        Node(1, move_random),
        Node(1, set_A),
        Node(1, set_B),
        Node(1, set_C),
        Node(1, set_D)
    ],
    connections=[
        
    ],
    max_conn=4,
    max_internal=4
)

world : World = World(width=255, height=255)

pop_size = 1000
num_generations : int = 50
generation_duration : int = 300

population : list[LittleGuy] = []
for g in range(num_generations):
    print(f'--------------')
    print(f'generation {str(g).zfill(3)}')
    
    if g == 0:
        # Place all the individuals in the population.
        for _ in range(pop_size):
            p = LittleGuy(world)
            p.brain = copy.deepcopy(STOCK_BRAIN)
            p.randomize()
            population.append(p)
    else:
        population = repopulate(population)
    
    for t in range(generation_duration):
        world.age = t / (generation_duration - 1)
        
        # Make every individual choose its next action.
        for p in population:
            transformation, activation = p.brain.evaluate(p)
            transformation(p, activation)
        
    # Kill everything in the left half of the world.
    # also removes the guys that have died from the population
    killed : int = world.kill(population, 0, 0, world.width // 2, world.height)
    print(f'{100 * round(1 - (killed / pop_size), 4)}% survival')