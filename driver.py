import matplotlib.pyplot as plt

from LittleGuy import LittleGuy
from World import World
from visual import AnimWriter

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
        p = LittleGuy(world)
        p.brain = copy.deepcopy(r.choice(current_pop).brain)
        
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
def export(world_states : list[list[str]], file_name : str) -> None:
    string : str = ''
    for gen in range(len(world_states)):
        for step in range(len(world_states[gen])):
            string += world_states[gen][step]
            if step != len(world_states[gen]) - 1:
                string += '.'
        if gen != len(world_states) - 1:
            string += '\n'
        
    f = open(f"{file_name}.dat", "w")
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

world : World = World(width=255 if len(sys.argv) < 5 else int(sys.argv[4]), height=255 if len(sys.argv) < 5 else int(sys.argv[4]))

pop_size : int = 1000 if len(sys.argv) < 2 else int(sys.argv[1])
num_generations : int = 250 if len(sys.argv) < 3 else int(sys.argv[2])
generation_duration : int = 300 if len(sys.argv) < 4 else int(sys.argv[3])

world_states : list[list[str]] = []
survival_rates : list[float] = [0] * num_generations

presence_of_move_right : list[float] = [0] * num_generations

population : list[LittleGuy] = []
for g in range(num_generations):
    if len(population) == 0 and g > 0:
        break

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
    survival_rates[g] = 1 - (killed / pop_size)
    print(f'{int(10000 * survival_rates[g]) / 100}% survival')
    world_states.append(gen_state)

    if len(population) == 0:
        break

    sum = 0
    for p in population:
        for c in p.brain.connections:
            if c.output == 7:
                sum += 1
                break
    presence_of_move_right[g] = sum / len(population)

file = uuid.uuid4()

export(world_states, file)

x = range(num_generations)
fig, ax = plt.subplots()

ax.plot(x, presence_of_move_right, linewidth=2, label='prominance of move_right gene', linestyle='dotted')
ax.plot(x, survival_rates, linewidth=2, label='survival')
ax.set(xlabel='generation', ylabel='survival', title='Survival rates over time', xlim=(0, num_generations - 1), ylim=(0, 1.1), xticks=np.arange(0, num_generations, num_generations // 10), yticks=np.arange(0, 1.1, 0.1))

ax.grid()
fig.legend()

fig.savefig(f'{file}.png')
print(file)
AnimWriter.Visualize(f'{file}.dat')
