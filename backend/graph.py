
class Graph:
    def __init__(self):
        self.adj_list = {}
        
    def add_node(self,node):
        if node not in self.adj_list:
            self.adj_list[node] = set()
    
    def add_edge(self, node_start, node_end, cost):
        if node_start not in self.adj_list:
            self.add_node(node_start)
        if node_end not in self.adj_list:
            self.add_node(node_end)
        self.adj_list[node_start].add((node_end,cost))

    def add_multiple_edges(self, edge_list):
        for edge in edge_list:
            self.add_edge(edge[0], edge[1], edge[2])
    
    def print_graph(self):
        for node in self.adj_list:
            for dest in self.adj_list[node]:
                print("Edge: ",node, dest[0], dest[1])
    
    def has_edge(self, start, end):
        if start not in self.adj_list:
            return -1
        for node,weight in self.adj_list[start]:
            if node == end:
                return weight
        return -1
