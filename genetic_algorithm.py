# This file contains code used to implement the genetic algorithm.
from copy import deepcopy
from project import CSE6140Project

import networkx as nx
import numpy as np
import random
import time

class genetic_algorithm():


	def __init__(s, G):
		s.G = G.Graph
		s.total_generations = 200
		s.pop_size = 50
		s.tournament_size = 6
		s.mutation_rate = .015

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
		count = 0
		for i in xrange(s.pop_size):
			for j in xrange(len(new_pop[i])):
				if random.random() < s.mutation_rate:
					#k = random.randint(0, len(new_pop[i])-1)
					#print new_pop[i],
					old_cost = s.get_cost(new_pop[i])
					new_cost = old_cost + 1

					check = 1
					while(new_cost>old_cost):
						indices = random.sample(range(len(new_pop[i])),2)
						i1,i2 = min(indices), max(indices)
						mutated_tour = new_pop[i][:i1] + [c for c in reversed(new_pop[i][i1:i2+1])] + new_pop[i][i2+1:]
						new_cost = s.get_cost(mutated_tour)
						check +=1
						if check>100:
							break
					new_pop[i] = mutated_tour
					#print new_pop[i],i1,i2
					#new_pop[i][j], new_pop[i][k] = new_pop[i][k], new_pop[i][j]
					count += 1
		#print count,
		return new_pop


	def main(s,filename,method,random_seed,cutoff_time,runID):
		start_time = time.time()
		population = s.get_initial_population()
		initial_cost = s.get_cost(s.find_fittest(population))
		print "Initial Cost: ", initial_cost
		current_best_cost = initial_cost
		all_costs = []

		with open('./'+filename[:-4]+'_'+method+'_'+str(cutoff_time)+runID+'.trace','w') as fil:

			for i in xrange(s.total_generations):
				cost = s.get_cost(s.find_fittest(population))

				all_costs.append(cost)

				if len(np.unique(np.array(all_costs[-6:])))==1 and len(all_costs)>10:
					break
				print i, cost
				if cost<current_best_cost:
					fil.write(str(round(time.time()-start_time,2))+','+str(int(cost))+'\n')
					current_best_cost = cost
				population = s.evolve(deepcopy(population))

			best_tour = s.find_fittest(population)
			final_cost = s.get_cost(best_tour)

			if final_cost<current_best_cost:
				fil.write(str(round(time.time()-start_time,2))+','+str(int(final_cost))+'\n')
			print "Final Cost: ", final_cost
			return best_tour,final_cost,time.time()-start_time


def run_genetic_algorithm(filename,method,random_seed,cutoff_time,runID):
	random.seed(random_seed)

	G = CSE6140Project()
	G.load_file(filename)
	print G.parameters
	ga = genetic_algorithm(G)
	best_tour,final_cost,runtime = ga.main(filename,method,random_seed,cutoff_time,runID)

	"""
	output = []
	times = []
	for i in xrange(5):
		ga = genetic_algorithm(G)
		start_time = time.time()
		output.append(ga.main())
		end_time = time.time()
		times.append(end_time-start_time)
	print output
	print np.mean(output)
	print (float)(np.mean(output)-float(G.parameters['optimal_cost']))/float(G.parameters['optimal_cost'])
	print times
	print np.mean(times)
	"""
	return best_tour,final_cost,runtime
