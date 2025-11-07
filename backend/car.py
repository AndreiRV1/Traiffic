from backend.graph import Graph
import random

class Car:
    id_crt = 0
    def __init__(self, graph : Graph):
        self.id = id
        self.id_crt += 1
        self.progress = 0
        self.speed = 5
        self.accelerate = 0
        self.graph = graph
        self.crt_note = list(self.graph.adj_list.keys())[random.randrange(1,len(graph.adj_list))]
        self.dest = list(self.graph.adj_list.keys())[random.randrange(1,len(graph.adj_list))]
        self.path = graph.traverse(self.crt_note,self.dest)
        self.next_node = self.path[1]
        self.crt_cost = self.graph.has_edge(self.crt_note, self.next_node)

    def update(self,dt):
        if self.crt_note == self.dest:
            return
        
        self.progress += self.speed * dt
        
        if self.progress >= self.crt_cost:
            self.crt_note = self.next_node
            self.progress = 0
            try:
                self.next_node = self.path[self.path.index(self.next_node) + 1]
                self.crt_cost = self.graph.has_edge(self.crt_note, self.next_node)
            except:
                self.next_node = self.next_node




