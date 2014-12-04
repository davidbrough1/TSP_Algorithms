import time
import random as random
import math as math
import os
from approximation import _get_solution
from project import CSE6140Project


def run_simulated_annealing(filename, cutoff_time, random_seed):
    file_name = str(filename[:-4]) + '_LS2_' + str(cutoff_time) + \
        '_' + str(random_seed) + '.trace'
    if os.path.isfile(file_name):
        os.remove(file_name)
    project = CSE6140Project()
    project.load_file(filename)
    return simulated_annealing(project.Graph, int(random_seed), file_name)


def simulated_annealing(G, random_seed, file_name):
    '''
    '''
    trace = open(file_name, 'a')
    t_start = time.time()
    random.seed(random_seed)
    edge_dict = _make_edge_dict(list(G.edges_iter(data=True)))
    temp_inital = 10000
    temp = 0.999999999999999999
    temp_power = 1
    initial_state = _get_solution(G)
    trace_str = str((time.time() - t_start,
                    int(_get_solution_weights(initial_state))))
    trace.write(trace_str[1:-1] + '\n')
    state = initial_state
    solution_steady_state_count = 0
    while solution_steady_state_count < len(initial_state) * 10:
        new_state, temp, temp_power = _annealing(state[:], edge_dict,
                                                 temp, temp_inital, temp_power)
        if new_state == state:
            solution_steady_state_count += 1
        else:
            if _get_solution_weights(new_state) < _get_solution_weights(state):
                state = new_state
                runtime = time.time() - t_start
                trace_str = str((runtime, int(_get_solution_weights(state))))
                trace.write(trace_str[1:-1] + '\n')
                solution_steady_state_count = 0
    tour = get_tour(state)
    return tour, int(_get_solution_weights(state)), runtime


def _annealing(state, edge_dict, temp, temp_inital, temp_power):
    '''
    This function takes in a state, the edge dictionary, the temp, initial
    temp and the power of the exponent used to determine the temp.
    '''
    edge_pair = _get_edge_pair(state)
    new_edge_pair = _get_new_edge_pair(edge_pair[0], edge_pair[1], edge_dict)
    del_E = _get_solution_weights(new_edge_pair) - \
        _get_solution_weights(edge_pair)
    if not new_edge_pair[0] in state and not new_edge_pair[1] in state:
        temp = temp ** temp_power
        if del_E < 0:
            tmp_state = _swap_edges(edge_pair, new_edge_pair, state[:])
        else:
            current_temp = temp_inital * temp ** temp_power
            if del_E == 0 or current_temp == 0:
                pass
            elif current_temp == 0.:
                if random.uniform(0, 1) > math.exp(current_temp / del_E):
                    tmp_state = _swap_edges(edge_pair, new_edge_pair, state[:])
            else:
                temp_power += 1
                if random.uniform(0, 1) < math.exp(- del_E / current_temp):
                    tmp_state = _swap_edges(edge_pair,
                                            new_edge_pair, state[:])
    if 'tmp_state' in locals():
        if _check_if_cycle(tmp_state):
            state = tmp_state
    return state, temp, temp_power


def _swap_edges(old_edge_pair, new_edge_pair, state):
    '''
    Changes 2 axes in a solution.
    '''
    index_0 = state.index(old_edge_pair[0])
    index_1 = state.index(old_edge_pair[1])
    state[index_0] = new_edge_pair[0]
    state[index_1] = new_edge_pair[1]
    return state


def _make_edge_dict(edge_list):
    '''
    Creates a diction with edges as keys and their weights as the values.
    '''
    edge_dict = {}
    for edge in edge_list:
        edge_dict[(edge[0], edge[1])] = edge[2]['weight']
    return edge_dict


def _get_solution_weights(solution_list):
    '''
    Gets solution weights.
    '''
    return sum([i[2] for i in solution_list])


def _get_edge_pair(edge_list):
    '''
    Gets 2 random edges from an edge_list.
    '''
    edge_indices = (random.randint(0, len(edge_list) - 1),
                    random.randint(0, len(edge_list) - 1))
    while edge_indices[0] == edge_indices[1]:
        edge_indices = (random.randint(0, len(edge_list) - 1),
                        random.randint(0, len(edge_list) - 1))
    return (edge_list[edge_indices[0]], edge_list[edge_indices[1]])


def _get_new_edge_pair(edge_0, edge_1, edge_dict):
    '''
    Creates a new edge pair from the original 2 edges provided.
    '''
    new_keys = _get_new_keys(edge_0, edge_1, edge_dict)
    edge_0_weight = edge_dict[new_keys[0]]
    edge_1_weight = edge_dict[new_keys[1]]
    return new_keys[0] + (edge_0_weight,), new_keys[1] + (edge_1_weight,)


def _get_new_keys(edge_0, edge_1, edge_dict):
    '''
    Gets 2 new edges without the weights from the given two edges.
    '''
    if edge_0[0] == edge_1[1] and edge_0[1] == edge_1[0] or \
            edge_0[0] == edge_1[0] and edge_0[1] == edge_1[1]:
        key0 = _check_key(edge_0[:-1], edge_dict)
        key1 = _check_key(edge_0[:-1], edge_dict)
        return key0, key1
    elif edge_0[0] == edge_1[0] or edge_0[1] == edge_1[1]:
        key1 = _check_key((edge_0[1], edge_1[0]), edge_dict)
        key0 = _check_key((edge_0[0], edge_1[1]), edge_dict)
        return key0, key1
    elif edge_0[0] == edge_1[1] or edge_0[1] == edge_1[0]:
        key1 = _check_key((edge_0[1], edge_1[1]), edge_dict)
        key0 = _check_key((edge_0[0], edge_1[0]), edge_dict)
        return key0, key1
    else:
        key1 = _check_key((edge_0[1], edge_1[1]), edge_dict)
        key0 = _check_key((edge_0[0], edge_1[0]), edge_dict)
        return key0, key1


def _check_key(key, edge_dict):
    '''
    Checks that target and source nodes are same order as those in edge_dict.
    '''
    if key in edge_dict.keys():
        return key
    else:
        new_key = (key[1],) + (key[0],)
        if new_key in edge_dict.keys():
            return new_key
        else:
            raise RuntimeError('Not a valid key %s' % str(key))


def _check_if_cycle(state):
    '''
    Helper function to check if new state is still a simple cycle.
    '''
    node_list = _get_node_list(state)
    if len(node_list) - 1 == len(state):
        return True
    else:
        return False


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
