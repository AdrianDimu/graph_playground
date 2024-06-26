# G = (V, E)
from collections import namedtuple
from itertools import combinations

from pyvis.network import Network

Graph = namedtuple("Graph", ["nodes", "edges", "is_directed"])

nodes = range(4)
edges = [
    (0, 1), 
    (0, 1), 
    (0, 2), 
    (0, 2), 
    (0, 3), 
    (1, 3), 
    (2, 3)]

G = Graph(nodes, edges, True)

def adjacency_dict(graph):
    """
    Returns the adjecency list representaiton of the graph.
    """
    adj = {node: [] for node in graph.nodes}
    for edge in graph.edges:
        node1, node2 = edge[0], edge[1]
        adj[node1].append(node2)
        if not graph.is_directed:
            adj[node2].append(node1)
    return adj

def adjacency_matrix(graph):
    """
    Returns the adjecency matrix of the graph.
    
    Assumes that graph.nodes is equivalent to range(len(graph.nodes)).
    """
    adj = [[0 for node in graph.nodes] for node in graph.nodes]
    for edge in graph.edges:
        node1, node2 = edge[0], edge[1]
        adj[node1][node2] += 1
        if not graph.is_directed:
            adj[node2][node1] += 1
    return adj

def show(graph, output_filename):
    """
    Saves a HTML file locally containing a visualization of the graph, 
    and returns a pyvis Network instance of the graph.
    """
    g = Network(directed=graph.is_directed)
    g.add_nodes(graph.nodes)
    g.add_edges(graph.edges)
    g.show(output_filename, notebook=False)
    return g

def _validate_num_nodes(num_nodes):
    """
    Check whether or not 'num_nodes' is a positive integer,
    and raises TypeError or ValueError if it's not.
    """
    if not isinstance(num_nodes, int):
        raise TypeError(f"num_nodes must be an integer; {type(num_nodes)=}")
    if num_nodes < 1:
        raise ValueError(f"num_nodes must be positive; {num_nodes=}")
    

def path_graph(num_nodes, is_directed=False):
    """
    Return a Graph instance representing
    a path in 'num_nodes' nodes.
    Can generate both directed and undirected graphs.
    """
    _validate_num_nodes(num_nodes)
    nodes = range(num_nodes)
    edges = [(i, i+1) for i in range(num_nodes - 1)]
    return Graph(nodes, edges, is_directed=is_directed)

def cycle_graph(num_nodes, is_directed=False):
    """
    Return a Graph instance representing
    a cycle in 'num_nodes' nodes.
    Can generate both directed and undirected graphs.
    """
    base_path = path_graph(num_nodes, is_directed)
    base_path.edges.append((num_nodes -1, 0))
    return base_path

def complete_graph(num_nodes):
    """
    Return a Graph instance representing
    a complete graph in 'num_nodes' nodes.
    Only undirected graphs.
    """
    _validate_num_nodes(num_nodes)
    nodes =  range(num_nodes)
    edges = list(combinations(nodes, 2))
    return Graph(nodes, edges, is_directed=False)

def star_graph(num_nodes):
    """
    Return a Graph instance representing
    the star graph in 'num_nodes' nodes.
    Only undirected graphs.
    """
    _validate_num_nodes(num_nodes)
    nodes =  range(num_nodes)
    edges = [(0, i) for i in range(1, num_nodes)]
    return Graph(nodes, edges, is_directed=False)

def _degrees(graph):
    """Return a dictionary of degrees for each node in the graph."""
    adj_list = adjacency_dict(graph)
    degrees = { 
        node: len(neighbors) 
        for node, neighbors in adj_list.items()
    }
    return degrees

def degrees(graph):
    """Return a dictionary of degrees for each node in an undirected graph."""
    if graph.is_directed:
        raise ValueError("Cannot call degrees() on a directed graph")
    return _degrees(graph)

def out_degrees(graph):
    """Return a dictionary of out degrees for each node in a directed graph."""
    if graph.is_directed:
        return _degrees(graph)
    raise ValueError("Cannot call out_degrees() on an undirected graph")

def total_degrees(graph):
    """Return a dictionary of total degrees for each node in a directed graph."""
    if not graph.is_directed:
        raise ValueError("Cannot call total_degrees() on an undirected graph")
    
    undirected_graph = Graph(graph.nodes, graph.edges, is_directed=False)
    return degrees(undirected_graph)

def in_degrees(graph):
    """Return a dictionary of in degrees for each node in a directed graph."""
    if not graph.is_directed:
        raise ValueError("Cannot call total_degrees() on an undirected graph.")
    
    reversed_edges = [(node2, node1) for node1, node2 in graph.edges]
    reversed_graph = Graph(graph.nodes, reversed_edges, is_directed=True) 
    return out_degrees(reversed_graph)

def min_degree(graph):
    """Return minimum degree for an undirected graph."""
    return min(degrees(graph).values())

def min_out_degree(graph):
    """Return minimum out degree for a directed graph."""
    return min(out_degrees(graph).values())

def min_in_degree(graph):
    """Return minimum in degree for a directed graph."""
    return min(in_degrees(graph).values())

def min_total_degree(graph):
    """Return minimum total degree for a directed graph."""
    return min(total_degrees(graph).values())

def max_degree(graph):
    """Return maximum degree for an undirected graph."""
    return max(degrees(graph).values())

def max_out_degree(graph):
    """Return maximum out degree for a directed graph."""
    return max(out_degrees(graph).values())

def max_in_degree(graph):
    """Return maximum in degree for a directed graph."""
    return max(in_degrees(graph).values())

def max_total_degree(graph):
    """Return maximum total degree for a directed graph."""
    return max(total_degrees(graph).values())