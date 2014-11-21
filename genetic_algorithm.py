from copy import deepcopy
from project import CSE6140Project

import networkx as nx
import random


class genetic_algorithm():


	def __init__(s, G):
		s.G = G.Graph		
		s.total_generations = 50
		s.pop_size = 50
		s.tournament_size = 6
		s.mutation_rate = 0.015

	def shuffle_tour(s):
		arrangement = range(1, s.G.number_of_nodes()+1)
		random.shuffle(arrangement)
		return arrangement


	def get_initial_population(s):
		return [s.shuffle_tour() for i in xrange(s.pop_size)]		


	def get_cost(s, tour):
		cost = sum([s.G[tour[i]][tour[i+1]]['weight'] for i in xrange(len(tour)-1)])
		cost += s.G[tour[0]][tour[-1]]['weight']
		return cost


	def find_fittest(s, population):
		costs = [s.get_cost(tour) for tour in population]
		min_cost_index = costs.index(min(costs))
		return population[min_cost_index]


	def tournament_select(s, population):
		sub_population = random.sample(population, s.tournament_size)
		min_cost_tour = s.find_fittest(sub_population)
		return min_cost_tour


	def crossover(s, p1, p2):
		if p1 == p2:
			return p1

		p3 = deepcopy(p2)
		indices = random.sample(range(1,len(p1)-1), 2)

		i,j = min(indices), max(indices)

		for loc in p1[i:j]:
			p2.remove(loc)
			
		return p2[0:i]+p1[i:j]+p2[i:]


	def evolve(s, population):
		new_pop = []

		#keep best from previous generation
		new_pop.append(s.find_fittest(population))
		
		for i in xrange(s.pop_size-1):
			parent1 = s.tournament_select(deepcopy(population))
			parent2 = s.tournament_select(deepcopy(population))
			
			new_pop.append(s.crossover(parent1, parent2))
		"""
		for i in xrange(s.pop_size):
			for j in xrange(len(new_pop[i])):
				if 
		"""

		return new_pop


	def main(s):
		population = s.get_initial_population()
		print "Initial Cost: ", s.get_cost(s.find_fittest(population))

		for i in xrange(s.total_generations):
			print i, s.get_cost(s.find_fittest(population))
			
			population = s.evolve(deepcopy(population))

		print "Final Cost: ", s.get_cost(s.find_fittest(population))


G = CSE6140Project()
G.load_file('berlin52.tsp')

ga = genetic_algorithm(G)
ga.main()