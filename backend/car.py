from backend.graph import Graph
import random

class Car:
    id_crt = 0
    def __init__(self, graph : Graph, spawners : list):
        self.id = id
        self.id_crt += 1
        self.progress = 0
        self.speed = 5
        self.accelerate = 0
        self.graph = graph
        self.crt_node, self.dest = random.sample(spawners,2)
        self.path = graph.traverse(self.crt_node,self.dest)
        self.next_node = self.path[1]
        self.crt_cost = self.graph.has_edge(self.crt_node, self.next_node)

# Function will update current instance of car, returning 0  when car reached destination and 1 else
    def update(self, dt : float):
        if self.crt_node == self.dest:
            return 0
        
        self.progress += self.speed * dt
        
        if self.progress >= self.crt_cost:
            self.crt_node = self.next_node
            self.progress = 0
            try:
                self.next_node = self.path[self.path.index(self.next_node) + 1]
                self.crt_cost = self.graph.has_edge(self.crt_node, self.next_node)
            except:
                self.next_node = self.next_node
        return 1




