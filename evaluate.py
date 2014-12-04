import wrapper_code
import numpy as np
import random

cutoff_time = '20000'
method = 'LS1'
random_seeds = random.sample(range(1,100),10)
avg_costs = []
avg_times = []

for filename in ['gr202.tsp','ulysses16.tsp','berlin52.tsp','burma14.tsp','kroA100.tsp','ch150.tsp']:
	costs = []
	times = []
	for seed in random_seeds:
		args = [filename,cutoff_time,method,str(seed)]
		print args
		cost,runtime = wrapper_code.main(args)
		costs.append(cost)
		times.append(runtime)

	avg_cost = np.mean(costs)
	avg_time = np.mean(times)
	avg_costs.append(avg_cost)
	avg_times.append(avg_time)
	print '\n\n\n\n'
	print costs
	print avg_costs
	print times
	print avg_times
	print '\n\n\n\n'

#burma14.tsp', 3350, 1.36, 0.0081
#'ulysses16.tsp', 6918, 1.86, 0.0086
#'berlin52.tsp', 8126, 20.42, 0.08
#'kroA100.tsp', 23979, 135.21, 0.12
#'ch150.tsp', 9121, 229.86, 0.39
#'gr202.tsp', 58080, 303.33, 0.45

#burma14.tsp', 3428, 0.0024, 0.031
#'ulysses16.tsp', 7049, 0.0052, 0.027
#'berlin52.tsp', 8100, 0.12, 0.073
#'kroA100.tsp', 24466, 0.58, 0.15
#'ch150.tsp', 7514, 1.82, 0.15
#'gr202.tsp', 45432, 3.99, 0.13
