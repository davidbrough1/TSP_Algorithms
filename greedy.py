'This file contains the code used to implement the greedy heuristic'
from project import CSE6140Project

import random
import time


class greedy():

    def __init__(s, G):
        s.G = G.Graph
        s.nodes = s.G.nodes()
        s.tour = []

    def dist(s, n1, n2):
        return s.G[n1][n2]['weight']

    def arc_dist(s, i, j, r):
        return s.G[i][r]['weight'] + s.G[r][j]['weight'] - s.G[i][j]['weight']

    def tour_cost(s, tour):
        cost = sum([s.G[tour[i]][tour[i + 1]]['weight']
                    for i in xrange(len(tour) - 1)])
        cost += s.G[tour[0]][tour[-1]]['weight']
        return cost

    def main(s, filename, method, random_seed, cutoff_time, runID, start_time):
        with open('./' + filename[:-4] + '_' + method + '_' + str(cutoff_time) + runID + '.trace', 'w') as fil:
            start_node = s.nodes.pop(random.randint(0, len(s.nodes) - 1))

            s.tour.append(start_node)

            distances = [s.dist(node, start_node) for node in s.nodes]
            max_idx = distances.index(max(distances))

            s.tour.append(s.nodes.pop(max_idx))

            while(s.nodes):
                candidate_costs = []
                for candidateN in s.nodes:
                    costs = [s.dist(visitedN, candidateN)
                             for visitedN in s.tour]
                    candidate_costs.append(max(costs))

                max_cost_idx = candidate_costs.index(max(candidate_costs))
                r = s.nodes.pop(max_cost_idx)

                arc_costs = []
                for i, j in zip(s.tour, s.tour[1:] + [s.tour[0]]):
                    arc_costs.append(s.arc_dist(i, j, r))

                split_idx = arc_costs.index(min(arc_costs))

                s.tour = s.tour[:split_idx + 1] + [r] + s.tour[split_idx + 1:]

            best_tour = s.tour
            final_cost = s.tour_cost(best_tour)
            fil.write(
                str(round(time.time() - start_time, 2)) + ',' + str(int(final_cost)) + '\n')
            print "Final Cost: ", final_cost
            return best_tour, final_cost


def run_greedy_algorithm(filename, method, random_seed, cutoff_time, runID):

    random.seed(random_seed)

    G = CSE6140Project()
    G.load_file(filename)
    print G.parameters

    start_time = time.time()
    gred = greedy(G)
    best_tour, final_cost = gred.main(
        filename, method, random_seed, cutoff_time, runID, start_time)
    return best_tour, final_cost, time.time() - start_time
