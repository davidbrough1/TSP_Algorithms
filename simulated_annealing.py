from approximation import _get_solution
import time
import random as random
import math as math


def simulated_annealing(G):
    t_start = time.time()
    edge_dict = _make_edge_dict(list(G.edges_iter(data=True)))
    temp = 0.9999
    initial_state = _get_solution(G)
    print 'intial weights', _get_solution_weights(initial_state)
    state = initial_state
    solution_steady_state_count = 0
    while solution_steady_state_count < 40:
        new_state, temp = _annealing(state, edge_dict, temp)
        if new_state == state:
            solution_steady_state_count += 1
        state = new_state
    print time.time() - t_start, _get_solution_weights(state)
    if _get_solution_weights(state) < 3323:
        print state


def _annealing(state, edge_dict, temp):
    edge_pair = _get_edge_pair(state)
    new_edge_pair = _get_new_edge_pair(edge_pair[0], edge_pair[1], edge_dict)
    del_E = _get_solution_weights(edge_pair) - \
        _get_solution_weights(new_edge_pair)
    if del_E > 0:
        temp = temp ** 1.5
        state = _swap_edges(edge_pair, new_edge_pair, state)
    else:
        if temp == 0. or del_E == 0:
            pass
        elif temp == 0.:
            if random.uniform(0, 1) < math.exp(- temp / del_E):
                temp = temp ** 3
                state = _swap_edges(edge_pair, new_edge_pair, state)
        elif del_E == 0:
            if random.uniform(0, 1) < math.exp(del_E / temp):
                temp = temp ** 3
                state = _swap_edges(edge_pair, new_edge_pair, state)
    return state, temp


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


def _get_new_edge_pair(edge_1, edge_2, edge_dict):
    '''
    '''
    new_keys = _get_new_keys(edge_1, edge_2, edge_dict)
    edge_0_weight = edge_dict[new_keys[0]]
    edge_1_weight = edge_dict[new_keys[1]]
    return new_keys[0] + (edge_0_weight,), new_keys[1] + (edge_1_weight,)


def _get_new_keys(edge_1, edge_2, edge_dict):
    if edge_1[0] == edge_2[1] and edge_1[1] == edge_2[0] or \
            edge_1[0] == edge_2[0] and edge_1[1] == edge_2[1]:
        return _check_key(edge_1[:-1], edge_2[:-1], edge_dict)
    elif edge_1[0] == edge_2[0] or edge_1[1] == edge_2[1]:
        key1 = _check_key((edge_1[1], edge_2[0]), edge_dict)
        key0 = _check_key((edge_1[0], edge_2[1]), edge_dict)
        return key0, key1
    elif edge_1[0] == edge_2[1] or edge_1[1] == edge_2[0]:
        key1 = _check_key((edge_1[1], edge_2[1]), edge_dict)
        key0 = _check_key((edge_1[0], edge_2[0]), edge_dict)
        return key0, key1
    else:
        key1 = _check_key((edge_1[1], edge_2[1]), edge_dict)
        key0 = _check_key((edge_1[0], edge_2[0]), edge_dict)
        return key0, key1


def _check_key(key, edge_dict):
    if key in edge_dict.keys():
        return key
    else:
        new_key = (key[1],) + (key[0],)
        if new_key in edge_dict.keys():
            return new_key
        else:
            raise RuntimeError('Not a valid key %s' % str(key))
