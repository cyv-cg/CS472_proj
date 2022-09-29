from World import World
from LittleGuy import LittleGuy

world : World = World(width=8, height=8)
population : list[LittleGuy] = []
for _ in range(1):
    population.append(LittleGuy(world))
for p in population:
    p.place_radomly()

world.print_matrix()

for _ in range(5):
    print()
    population[0].move_random()
    world.print_matrix()