import sys
from genetic_algorithm import *
from greedy import *
from timeout import timeout

@timeout(int(sys.argv[2]))
def main(args):
	filename = args[0]
	cutoff_time = int(args[1])
	method = args[2]
	random_seed = args[3]
	
	if method == 'LS1':
		tour,cost = run_genetic_algorithm(filename,random_seed)
		runID = '_'+str(random_seed)
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
	with open('op/'+filename[:-4]+'_'+method+'_'+str(cutoff_time)+runID+'.sol','w') as opfile:
		opfile.write(str(int(cost)))
		opfile.write('\n')
		opfile.write(','.join([str(c) for c in tour]))

if __name__ == '__main__':
	main(sys.argv[1:])