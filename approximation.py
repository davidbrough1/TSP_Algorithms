import Queue as q
import time
import networkx as nx
import random as random

def approximation(G):
    t_start = time.time()
    solution = _get_solution(G)
    return _get_solution_weights(solution), time.time() - t_start


def _get_solution(G):
    MST_edges = Kruskal(G)
    reverse_edges = [(x[1], x[0], x[2]) for x in MST_edges]
    edge_list = MST_edges + reverse_edges
    path_nodes = _depth_first_search(edge_list)
    edge_list = G.edges(data=True)
    return _get_path_edge_list(path_nodes, edge_list)


def _get_solution_weights(solution):
    weight = 0
    for edge in solution:
        weight += edge[2]
    return weight


def _get_path_edge_list(path_nodes, edge_list):
    path = []
    n_nodes = len(path_nodes)
    for edge in edge_list:
        for i in range(n_nodes):
            node_i = path_nodes[i]
            node_i_plus = path_nodes[(i + 1) % n_nodes]
            if edge[0] == node_i and edge[1] == node_i_plus:
                    path.append((edge[0], edge[1], edge[2]['weight']))
            elif edge[1] == node_i and edge[0] == node_i_plus:
                    path.append((edge[1], edge[0], edge[2]['weight']))
    return path


def _depth_first_search(edge_list):
    G_tmp = nx.Graph()
    G_tmp.add_weighted_edges_from(edge_list)
    edge_index = random.randint(0, len(edge_list) - 1)
    path_sequence = list(nx.dfs_preorder_nodes(G_tmp,
                                               edge_list[edge_index][0]))
    return path_sequence


def Kruskal(G):
    '''
    Kruskal' Algorithm

    1. Create a priority queue E with all edges with the weights as the key.
    2. Create empty list L that will be the list of connected nodes
    3. Create empty list E_list that has MST edges
    3. pop E
    4. Check to see if and add nodes connected to edge E (A, B) are in L.
    5. If A and B are in L return to step 3 else add any node not in L to it
       and add the edge to E.
    6. Repeat steps 3 through 5 until L contains all the nodes.
    '''
    L = []
    weights = _get_weights(G)
    edges = _get_edges(G)
    node_set = _make_sets(G.nodes())
    p_q = q.PriorityQueue(len(weights))
    [p_q.put((weights[ii],) + (edges[ii],)) for ii in range(len(weights))]
    MST_edge_list = []
    while len(MST_edge_list) < len(G.nodes()) - 1:
        tmp_edge = p_q.get()
        tmp_edge_tuple = (tmp_edge[1][0], tmp_edge[1][1], tmp_edge[0])
        set1 = _find_set(tmp_edge_tuple[0], node_set)
        set2 = _find_set(tmp_edge_tuple[1], node_set)
        if set1 != set2:
            L.append(tmp_edge_tuple[0])
            L.append(tmp_edge_tuple[1])
            MST_edge_list.append(tmp_edge_tuple)
            node_set.remove(set1)
            node_set.remove(set2)
            node_set.insert(0, set1.union(set2))
    return MST_edge_list


def _find_set(node, sets):
    '''
    finds set that contains the node.
    '''
    for s in sets:
        if node in s:
            return s


def _get_weights(G):
    """
    Returns a list of the weights in the graph.
    """
    Graph_data = list(G.edges_iter(data=True))
    return [Graph_data[ii][2]['weight'] for ii in range(len(Graph_data))]


def _get_weights_and_edges(G):
    """
    Returns a list of edge weights and the node pairs.
    """
    return list(G.edges_iter(data=True))


def _get_edges(G):
    """
    Returns a list of node pairs for each edge.
    """
    Graph_data = _get_weights_and_edges(G)
    return [Graph_data[ii][:-1] for ii in range(len(Graph_data))]


def _make_sets(nodes):
    '''
    Create disjointed set for each node.
    '''
    node_sets = []
    [node_sets.append(set([n])) for n in nodes]
    return node_sets
