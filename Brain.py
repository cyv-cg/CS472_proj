import random as r
import behaviors

class Node:
    transformation = lambda x: x
    
    _activation : float = 0
    _visited : bool = False
    
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
    
    MAX_CONNECTIONS : int = 0
    MAX_INTERNAL_NEURONS : int = 0
    
    def __init__(self, nodes : list[Node], connections : list[Connection], max_conn : int = 0, max_internal : int = 0) -> None:
        self.nodes = nodes
        self.connections = connections
        
        self.MAX_CONNECTIONS = max_conn
        self.MAX_INTERNAL_NEURONS = max_internal
    
    def reset_activations(self):
        for n in self.nodes:
            n._activation = 0
            n._visited = False
    
    # I don't know how this works but it does.
    # It's some kind of janky reverse DFS-style algorithm.
    def evaluate(self, agent) -> any:
        # Search through all connections in reverse (i.e. start at the outputs and recurse back to the inputs).
        for node in self.nodes:
            if node.neuron_type != 1:
                continue
            else:
                node._activation = self._eval_node(node, agent)
        # Find the most active neuron and return its function.
        max_activation : Node = None
        max_activations : list[Node] = []
        for n in self.nodes:
            # Only look for output neurons.
            if n.neuron_type != 1:
                continue
            if max_activation == None or n._activation > max_activation._activation:
                max_activation = n
        for n in self.nodes:
            if n.neuron_type != 1:
                continue
            if max_activation == None or n._activation == max_activation._activation:
                max_activations.append(n)
        self.reset_activations()
        choice = r.choice(max_activations)
        return choice.transformation, choice._activation
    def _eval_node(self, node : Node, agent) -> float:
        node._visited = True
        # Search all connections and find every node that outputs to the given node.
        inputs : list[Connection] = []
        for conn in self.connections:
            if self.nodes[conn.output] == node:
                inputs.append(conn)
        # Loop through each connection that leads into the given node.
        if len(inputs) > 0:
            activation_sum : float = 0
            for c in inputs:
                # No cycles.
                # Cycles bad.
                if c.input == c.output:
                    continue
                # Recursively evaluate input nodes and add together all their activations.
                # Avoid evaluating nodes more than once and remove cycles.
                # Technically, a node can have 0 activation and still have been activated, but it's not a big deal.
                if self.nodes[c.input]._activation != 0 or self.nodes[c.input]._visited:
                    activation_sum += self.nodes[c.input]._activation * c.weight
                else:
                    activation_sum += self._eval_node(self.nodes[c.input], agent) * c.weight
            # If this is an output neuron, then take the transformation to get the final activation.
            if node.neuron_type != 1:
                if node.neuron_type == 0:
                    node._activation = node.transformation(agent)
                elif node.neuron_type == 2:
                    node._activation = node.transformation(agent, activation_sum)
            # Apply the calculated activation to interior neurons.
            else:
                node._activation = activation_sum
        # If no such connections exist, then this is (most likely) an input node whose activation can be taken as is.
        elif node.neuron_type == 0:
            node._activation = node.transformation(agent)
        return node._activation
    
    def mutate(self, mutation_chance : float = 1/1000) -> None:
        internal_neurons = []
        for n in self.nodes:
            if n.neuron_type == 2:
                internal_neurons.append(n)

        if r.random() < mutation_chance and len(internal_neurons) > 0:
            n = r.choice(internal_neurons)
            i = -1
            for x in range(len(self.nodes)):
                if self.nodes[x] == n:
                    i = x
                    break
            for c in self.connections:
                if c.output == i or c.input == i:
                    self.connections.remove(c)
            self.nodes.remove(n)
            for c in self.connections:
                if c.input > i:
                    c.input -= 1
                if c.output > i:
                    c.output -= 1
        if r.random() < mutation_chance and len(internal_neurons) < self.MAX_INTERNAL_NEURONS:
            self.nodes.append(
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
            
        if r.random() < mutation_chance and len(self.connections) > 0:
            self.connections.remove(r.choice(self.connections))
        if r.random() < mutation_chance and len(self.connections) < self.MAX_CONNECTIONS:
            self.connections.append(
                    Connection(
                        input=r.choice(range(len(self.nodes))), 
                        output=r.choice(range(len(self.nodes))),
                        weight=10 * (2 * r.random() - 1)
                    )
                )

        for c in self.connections:
            if r.random() < mutation_chance:
                c.weight += 2 * r.random() - 1
            
            if r.random() < mutation_chance:
                c.input = r.choice(range(len(self.nodes)))
            if r.random() < mutation_chance:
                c.output = r.choice(range(len(self.nodes)))
