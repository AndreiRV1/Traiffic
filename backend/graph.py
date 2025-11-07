from heapq import heapify, heappop, heappush

class Graph:
    def __init__(self):
        self.adj_list = {}
        
    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = set()
    
    def add_edge(self, node_start, node_end, cost : float):
        if node_start not in self.adj_list:
            self.add_node(node_start)
        if node_end not in self.adj_list:
            self.add_node(node_end)
        self.adj_list[node_start].add((node_end,cost))
    
    def add_double_edge(self, node_start, node_end, cost : float):
        self.add_edge(node_start, node_end, cost)
        self.add_edge(node_end, node_start, cost)

    def add_multiple_edges(self, edge_list : list):
        try:
            for edge in edge_list:
                self.add_edge(edge[0], edge[1], edge[2])
        except:
            self.add_edge(edge_list[0], edge_list[1], edge_list[2])
            
            
    def add_multiple_edges_double(self, edge_list : list):
        for edge in edge_list:
            self.add_double_edge(edge[0], edge[1], edge[2])
    
    def print_graph(self):
        for node in self.adj_list:
            print("Node:",node)
            for dest in self.adj_list[node]:
                print("Neigh: ", dest[0], dest[1])
    
    def has_edge(self, start, end):
        if start not in self.adj_list:
            return -1
        for node,weight in self.adj_list[start]:
            if node == end:
                return weight
        return -1
    
    def traverse(self, start, end):
        distances = {node: (float("inf"), None) for node in self.adj_list }
        distances[start] = (0, None)
        found = 0
        heap = [(0,start,None)]
        heapify(heap)

        visited = set()

        while heap:
            crt_dist, crt_node,_ = heappop(heap)
            if crt_node not in visited:
                visited.add(crt_node)
                if crt_node == end:
                    found = 1
                    break
                
                for neigh, distance in self.adj_list[crt_node]:
                    new_distance = crt_dist + distance
                    if new_distance < distances[neigh][0]:
                        distances[neigh] = (new_distance,crt_node)
                        heappush(heap, (new_distance,neigh,crt_node))
        path = list()
        if found == 1:
            path.append(end)
            crt_node = end
            while distances[crt_node][1] != None:
                crt_node = distances[crt_node][1]
                path.append(crt_node)
        path = list(reversed(path))
        return path