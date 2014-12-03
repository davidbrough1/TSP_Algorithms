import wrapper_code
import numpy as np
import random

cutoff_time = '10000'
method = 'LS1'
random_seeds = random.sample(range(1,100),10)
avg_costs = []
avg_times = []

for filename in ['kroA100.tsp','ch150.tsp','gr202.tsp']:
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

#burma14.tsp', 3350, 1.36
#'ulysses16.tsp', 6918, 1.86
#'berlin52.tsp', 8126, 20.42