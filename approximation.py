# This file contains the code for the implementation of the MST approximation.
import Queue as q
import time
import networkx as nx
import random as random
import os
from project import CSE6140Project


def run_MSTApprox(filename, cutoff_time, random_seed):
    '''
    Helper function to integrate with TSP.py
    '''
    project = CSE6140Project()
    project.load_file(filename)
    file_name = str(filename[:-4]) + '_Approx_' + str(cutoff_time) + \
        '_' + str(random_seed) + '.trace'
    if os.path.isfile(file_name):
        os.remove(file_name)
    return approximation(project.Graph, file_name, random_seed)


def approximation(G, file_name, random_seed):
    '''
    This method takes in a graph and uses the MST approximation algorithm to
    find an approximate solution to TSP for a given tree.
    '''
    t_start = time.time()
    random.seed(random_seed)
    solution = _get_solution(G)
    runtime = time.time() - t_start
    tour = get_tour(solution)
    trace = open(file_name, 'a')
    cost = int(_get_solution_weights(solution))
    trace_str = str((runtime, cost))
    trace.write(trace_str[1:-1])
    return tour, cost, runtime


def _get_solution(G):
    '''
    This helper function returns the results from the MST approximation
    algorithm.
    '''
    MST_edges = Kruskal(G)
    reverse_edges = [(x[1], x[0], x[2]) for x in MST_edges]
    edge_list = MST_edges + reverse_edges
    path_nodes = _depth_first_search(edge_list)
    edge_list = G.edges(data=True)
    return _get_path_edge_list(path_nodes, edge_list)


def _get_solution_weights(solution):
    '''
    This function retuns the sum weights of a solution.
    '''
    weight = 0
    for edge in solution:
        weight += edge[2]
    return weight


def _get_path_edge_list(path_nodes, edge_list):
    '''
    This function get get the weights for the node path.
    '''
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
    '''
    This function does a depth first search of a graph with a random node
    selected as the root of a tree representing the graph.
    '''
    G_tmp = nx.Graph()
    G_tmp.add_weighted_edges_from(edge_list)
    edge_index = random.randint(0, len(edge_list) - 1)
    path_sequence = list(nx.dfs_preorder_nodes(G_tmp,
                                               edge_list[edge_index][0]))
    return path_sequence


def Kruskal(G):
    '''
    Kruskal' Algorithm - returns MST of the given graph G.

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


def get_tour(state):
    '''
    Get tour of graph starting with node v1, v2, v2, ..., vn, v1.
    '''
    node_list = _get_node_list(state)
    tour = [node_list[0]]
    for node in node_list[1:]:
        tour.append(node)
        tour.append(node)
    return tour[:-1]


def _get_node_list(state):
    tmp_state = state[:]
    first_edge = tmp_state.pop()
    node_list = [first_edge[0], first_edge[1]]
    while node_list.count(node_list[-1]) < 2:
        for edge in tmp_state:
            if edge[0] == node_list[-1]:
                tmp_state.remove(edge)
                node_list.append(edge[1])
            elif edge[1] == node_list[-1]:
                tmp_state.remove(edge)
                node_list.append(edge[0])
    return node_list
