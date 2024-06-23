import heapq
import sys

class Node:
    def __init__(self, val):
        self.val = val

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return str(self.val)

    def __lt__(self, node):
        return str(self.val) < str(node.val)

    def __le__(self, node):
        return str(self.val) <= str(node.val)
        
class Edge:
    def __init__(self, w, dest):
        self.dest = dest
        self.w = w

class DisjointSet:
    def __init__(self, nodes):
        self.nodes = {node: -1 for node in nodes}

    def find(self, node):
        if self.nodes[node] == -1:
            return node
        self.nodes[node] = self.find(self.nodes[node])
        return self.find(self.nodes[node])

    def union(self, a, b):
        parent_a = self.find(a)
        parent_b = self.find(b)
        if parent_a != parent_b or (parent_a==parent_b==-1):
            if self.nodes[parent_a] < self.nodes[parent_b]:
                self.nodes[parent_a] = parent_b
            else:
                self.nodes[parent_b] = parent_a
                
    def is_cycle(self, a, b):
        return self.find(a) == self.find(b)

class Graph:
    def __init__(self, adj_list):
        self.graph = adj_list

    def mst_prim(self):
        pass

    def mst_kruskal(self):
        cur_st = DisjointSet(self.graph.keys())
        edges = []
        vertices = set()
        sorted_edges = self.sort_edges()
        while len(edges) < len(self.graph)-1:
            cur_edge = sorted_edges.pop()
            w, end_points = cur_edge
            ep = list(end_points)
            if not cur_st.is_cycle(ep[0], ep[1]):
                cur_st.union(ep[0], ep[1])
                edges.append(cur_edge)
                vertices.add(ep[0])
                vertices.add(ep[1])
        return vertices, edges

    def sort_edges(self):
        zip_edges = [(edge.w, {node, edge.dest}) for node in self.graph for edge in self.graph[node]]
        filtered_edges = [zip_edges[0]]
        for edge in zip_edges:
            if edge not in filtered_edges:
                filtered_edges.append(edge)
        return sorted(filtered_edges, key=lambda edge: edge[0], reverse=True)        

    def dijkstra(self, start, end):
        self.distances = {node:(sys.maxsize, None) if node != start else (0, None) for node in self.graph}
        visited = set()
        pqueue = [(0, start)]
        heapq.heapify(pqueue)
        while len(visited) < len(self.graph):
            dist_node = heapq.heappop(pqueue)
            self.update_distances(dist_node, pqueue, visited)
            visited.add(dist_node)
        return self.find_path(end)

    def update_distances(self, dist_node, pq, visited):
        cur_dist, cur_node = dist_node
        for edge in self.graph[cur_node]:
            if edge.dest not in visited:
                new_dist = cur_dist + edge.w
                if new_dist < self.distances[edge.dest][0]:
                    self.distances[edge.dest] = (new_dist, cur_node)
                    heapq.heappush(pq, (new_dist, edge.dest))

    def find_path(self, node):
        if node not in self.graph:
            return 0, None
        path = [node]
        total_dist = self.distances[node][0]
        prev_node = self.distances[node][1]
        while prev_node:
            path.append(prev_node)
            total_dist += self.distances[prev_node][0]
            prev_node = self.distances[prev_node][1]
        return total_dist, path
    
A = Node("A")
B = Node("B")
C = Node("C")
D = Node("D")
E = Node("E")
F = Node("F")

adj_list = {A: [Edge(4, D), Edge(6, C), Edge(3, B)],
            B: [Edge(3, A), Edge(2, C), Edge(3, E)],
            C: [Edge(6, A), Edge(2, B), Edge(3, E), Edge(3, F)],
            D: [Edge(4, A), Edge(6, F)],
            E: [Edge(3, B), Edge(3, C), Edge(1, F)],
            F: [Edge(6, D), Edge(3, C), Edge(1, E)]
           }

graph = Graph(adj_list)
path, dist = graph.dijkstra(A, F)
vert, edges = graph.mst_kruskal()