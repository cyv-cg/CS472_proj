import random as r
import numpy as np

#################################################################################################################################################
# INPUT BEHAVIORS
#################################################################################################################################################

def pos_x(agent) -> float:
	return agent._x / agent._world.width
def pos_y(agent) -> float:
	return agent._y / agent._world.height

def rand(agent) -> float:
	return r.random() * 2 - 1

def check_time(agent) -> float:
	return agent._world.age

def check_forward(agent) -> int:
	return agent._world.check_cell(agent._x + agent._forward[0], agent._y + agent._forward[1])

def oscillator(agent) -> float:
    return np.sin(check_time(agent))

#################################################################################################################################################



#################################################################################################################################################
# OUTPUT BEHAVIORS
#################################################################################################################################################

# All the movement functions we could ever need.
def move_left(agent, activation : float) -> bool:
	return agent.set_coordinates(agent._x - 1, agent._y)
def move_right(agent, activation : float) -> bool:
	return agent.set_coordinates(agent._x + 1, agent._y)
def move_up(agent, activation : float) -> bool:
	return agent.set_coordinates(agent._x, agent._y - 1)
def move_down(agent, activation : float) -> bool:
	return agent.set_coordinates(agent._x, agent._y + 1)
def move_up_left(agent, activation : float) -> bool:
	return agent.set_coordinates(agent._x - 1, agent._y - 1)
def move_up_right(agent, activation : float) -> bool:
	return agent.set_coordinates(agent._x + 1, agent._y - 1)
def move_down_left(agent, activation : float) -> bool:
	return agent.set_coordinates(agent._x - 1, agent._y + 1)
def move_down_right(agent, activation : float) -> bool:
	return agent.set_coordinates(agent._x + 1, agent._y + 1)
def move_forward(agent, activation : float) -> bool:
	return agent.set_coordinates(agent._x + agent._forward[0], agent._y + agent._forward[1])
def move_reverse(agent, activation : float) -> bool:
	return agent.set_coordinates(agent._x - agent._forward[0], agent._y - agent._forward[1])
def move_random(agent, activation : float) -> bool:
	move = r.choice([move_left, move_right, move_up, move_down,
						move_up_left, move_up_right, move_down_left, move_down,
						move_forward, move_reverse
    ])
	return move(agent, activation)

def set_A(agent, activation : float) -> None:
    agent._A = activation
def set_B(agent, activation : float) -> None:
    agent._B = activation
def set_C(agent, activation : float) -> None:
    agent._C = activation
def set_D(agent, activation : float) -> None:
    agent._D = activation

#################################################################################################################################################



#################################################################################################################################################
# INTERNAL TRANSFORMATION FUNCTIONS
#################################################################################################################################################

def sigmoid(agent, activation : float) -> float:
    return agent._A / (1 + agent._B * np.exp(-activation * agent._C))

def step(agent, activation : float) -> float:
    return np.floor(agent._A * activation)

def abs(agent, activation : float) -> float:
    return np.abs(agent._D * activation)

def piece(agent, activation : float) -> float:
    return -agent._A * agent._B if activation < agent._C else agent._A * agent._B

def parabola(agent, activation : float) -> float:
    return (agent._D * activation) ** 2

#################################################################################################################################################