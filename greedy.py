from project import CSE6140Project

import random

class greedy():
	def __init__(s,G):
		s.G = G.Graph
		s.nodes = s.G.nodes()
		s.tour = []


	def dist(s,n1,n2):
		return s.G[n1][n2]['weight']


	def arc_dist(s,i,j,r):
		return s.G[i][r]['weight'] + s.G[r][j]['weight'] - s.G[i][j]['weight']


	def tour_cost(s, tour):
		cost = sum([s.G[tour[i]][tour[i+1]]['weight'] for i in xrange(len(tour)-1)])
		cost += s.G[tour[0]][tour[-1]]['weight']
		return cost


	def main(s):
		start_node = s.nodes.pop(random.randint(0,len(s.nodes)-1))		

		s.tour.append(start_node)

		distances = [s.dist(node, start_node) for node in s.nodes]
		max_idx = distances.index(max(distances))

		s.tour.append(s.nodes.pop(max_idx))

		while(s.nodes):
			candidate_costs = []
			for candidateN in s.nodes:
				costs = [s.dist(visitedN, candidateN) for visitedN in s.tour]
				candidate_costs.append(max(costs))
			
			max_cost_idx = candidate_costs.index(max(candidate_costs))
			r = s.nodes.pop(max_cost_idx)

			arc_costs = []
			for i,j in zip(s.tour, s.tour[1:]+[s.tour[0]]):
				arc_costs.append(s.arc_dist(i,j,r))

			split_idx = arc_costs.index(min(arc_costs))

			s.tour = s.tour[:split_idx+1] + [r] + s.tour[split_idx+1:]

		print s.tour_cost(s.tour)

G = CSE6140Project()
G.load_file('kroA100.tsp')
print G.parameters['optimal_cost']
gred = greedy(G)
gred.main()