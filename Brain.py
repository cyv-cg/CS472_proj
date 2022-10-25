from matplotlib.pyplot import connect
import numpy as np

class Node:
    transformation = lambda x: x
    
    _activation : float = 0
    _activated : bool = False
    
    # -1 = undefined
    # 0 = input
    # 1 = output
    # 2 = internal
    neuron_type : int = -1
    
    def __init__(self, type : int, transformation_function) -> None:
        self.transformation = transformation_function
        self.neuron_type = type

class Connection:
    weight : float = 0
    #active : bool = False
    
    input : int = -1
    output : int = -1
    
    def __init__(self, input : int, output : int, weight : float) -> None:
        self.weight = weight
        self.input = input
        self.output = output
    
    def set_active(self, active_state : bool) -> None:
        self.active = active_state

class Network:
    nodes : list[Node] = None
    connections : list[Connection] = None
    
    def __init__(self, nodes : list[Node], connections : list[Connection]) -> None:
        self.nodes = nodes
        self.connections = connections
    
    def reset_activations(self):
        for n in self.nodes:
            n._activation = 0
            n._activated = False
    
    # I don't know how this works but it does.
    # It's some kind of janky reverse DFS-style algorithm.
    def evaluate(self) -> any:
        # Search through all connections in reverse (i.e. start at the outputs and recurse back to the inputs).
        for node in self.nodes:
            if node.neuron_type != 1:
                continue
            else:
                node._activation = self._eval_node(node)
        # Find the most active neuron and return its function.
        max_activation : Node = None
        for n in self.nodes:
            # Only look for output neurons.
            if n.neuron_type != 1:
                continue
            if max_activation == None or n._activation > max_activation._activation:
                max_activation = n
        self.reset_activations()
        return max_activation.transformation
    def _eval_node(self, node : Node) -> float:
        # Search all connections and find every node that outputs to the given node.
        inputs : list[Connection] = []
        for conn in self.connections:
            if self.nodes[conn.output] == node:
                inputs.append(conn)
        # Loop through each connection that leads into the given node.
        if len(inputs) > 0:
            activation_sum : float = 0
            for c in inputs:
                # Recursively evaluate input nodes and add together all their activations.
                # Avoid evaluating nodes more than once.
                if self.nodes[c.input]._activated:
                    activation_sum += self.nodes[c.input]._activation * c.weight
                else:
                    activation_sum += self._eval_node(self.nodes[c.input]) * c.weight
            # If this is an output neuron, then take the transformation to get the final activation.
            if node.neuron_type != 1:
                node._activation = node.transformation(activation_sum)
            # Apply the calculated activation to interior neurons.
            else:
                node._activation = activation_sum
        # If no such connections exist, then this is (most likely) an input node whose activation can be taken as is.
        elif node.neuron_type == 0:
            node._activation = node.transformation()
        return node._activation