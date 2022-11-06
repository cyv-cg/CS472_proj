from LittleGuy import LittleGuy
from World import World

from behaviors import *
from Brain import *

import random as r
import numpy as np

import uuid

import copy
import sys

class WorldState:
    generations : list[list[np.array(int)]] = []

def repopulate(current_pop : list[LittleGuy]) -> list[LittleGuy]:
    for x in range(world.width):
        for y in range(world.height):
            if world.matrix[x, y] == world.ids['agent']:
                world.matrix[x, y] = world.ids['empty']
    
    population : list[LittleGuy] = []
    while len(population) < pop_size:
        # Randomly choose an individual to clone.
        p = copy.copy(r.choice(current_pop))
        
        # Place individual in the world.
        p._x = -1
        p._y = -1
        p.place_randomly()
        population.append(p)

        # Mutate the neural network.
        p.brain.mutate()

    return population

# Each row in the world is separated by a space
# Each timestep is separated by a .
# Each generation is separated by a new line
def export(world_states : list[list[str]]) -> None:
    string : str = ''
    for gen in range(len(world_states)):
        for step in range(len(world_states[gen])):
            string += world_states[gen][step]
            if step != len(world_states[gen]) - 1:
                string += '.'
        if gen != len(world_states) - 1:
            string += '\n'
        
    f = open(f"{uuid.uuid4()}.dat", "w")
    f.write(string)
    f.close()

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

pop_size : int = 100 if len(sys.argv) < 2 else int(sys.argv[1])
num_generations : int = 20 if len(sys.argv) < 3 else int(sys.argv[2])
generation_duration : int = 100 if len(sys.argv) < 4 else int(sys.argv[3])

world_states : list[list[str]] = []

population : list[LittleGuy] = []
for g in range(num_generations):
    print(f'--------------')
    print(f'generation {str(g).zfill(3)}')
    
    gen_state : list[str] = []

    if g == 0:
        # Place all the individuals in the population.
        for _ in range(pop_size):
            p = LittleGuy(world)
            p.brain = copy.deepcopy(STOCK_BRAIN)
            p.randomize()
            population.append(p)
    else:
        population = repopulate(population)
    
    if len(population) == 0:
        break

    for t in range(generation_duration):
        # Save a snapshot of the world in the moment.
        gen_state.append(world.matrix_to_str())
        
        world.age = t / (generation_duration - 1)
        
        # Make every individual choose its next action.
        for p in population:
            transformation, activation = p.brain.evaluate(p)
            transformation(p, activation)
        
    # Kill everything in the left half of the world.
    # also removes the guys that have died from the population
    killed : int = world.kill(population, 0, 0, world.width // 2, world.height)
    print(f'{int(10000 * (1 - (killed / pop_size))) / 100}% survival')
    world_states.append(gen_state)

export(world_states)