import sys
from genetic_algorithm import *
from greedy import *
from timeout import timeout

#@timeout(int(sys.argv[2]))
@timeout(100000)
def main(args):
	filename = args[0]
	cutoff_time = int(args[1])
	method = args[2]
	random_seed = args[3]
	
	if method == 'LS1':
		runID = '_'+str(random_seed)
		tour,cost,runtime = run_genetic_algorithm(filename,method,random_seed,cutoff_time,runID)
	elif method == 'BnB':
		runID = ''
	elif method == 'Heuristic':
		tour,cost = run_greedy_algorithm(filename,random_seed)
		runID = ''
	elif method == 'LS2':
		runID = '_'+str(random_seed)
	elif method == 'Approx':
		runID = ''
	else:
		print "Incorrect Method Entered. The correct options are:\nGA, BnB, Greedy, SA, Approx"

	#for runID in xrange(1,11):
	with open('op/'+filename[:-4]+'_'+method+'_'+str(cutoff_time)+runID+'.sol','w') as solfile:
		solfile.write(str(int(cost)))
		solfile.write('\n')
		solfile.write(','.join([str(c) for c in tour]))

	return cost,runtime

#if __name__ == '__main__':
#	main(sys.argv[1:])