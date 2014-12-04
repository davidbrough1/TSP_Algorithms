import sys, getopt
from genetic_algorithm import *
from greedy import *
from timeout import timeout
from tsp import *
#@timeout(100000)
@timeout(int(sys.argv[6]))
def main(args):
	try:
		opts, args = getopt.getopt(args,"hi:a:t:s:",["inst=","alg=","time=","seed="])
	except getopt.GetoptError:
		print 'python ./tsp.py --inst <filename.tsp> --alg [BnB | Approx | Heuristic | LS1 | LS2] --time <cutoff_in_seconds> --seed <random_seed>'
		sys.exit(2)

	for opt,arg in opts:
		if opt == '-h':
			print 'python ./tsp.py --inst <filename.tsp> --alg [BnB | Approx | Heuristic | LS1 | LS2] --time <cutoff_in_seconds> --seed <random_seed>'
			sys.exit()
		elif opt in ('-i','--inst'):
			filename = arg
		elif opt in ('-a','--alg'):
			method = arg
		elif opt in ('-t','--time'):
			cutoff_time = arg
		elif opt in ('-s','--seed'):
			random_seed = arg

	if method == 'LS1':
		runID = '_'+str(random_seed)
		tour,cost,runtime = run_genetic_algorithm(filename,method,random_seed,cutoff_time,runID)
	elif method == 'BnB':
		runID = ''
	elif method == 'Heuristic':
		tour,cost,runtime = run_greedy_algorithm(filename,random_seed)
		runID = ''
	elif method == 'LS2':
		runID = '_'+str(random_seed)
	elif method == 'Approx':
		runID = ''
	else:
		print "Incorrect Method Entered. The correct options are:\nGA, BnB, Greedy, SA, Approx"

	with open('check/'+filename[:-4]+'_'+method+'_'+str(cutoff_time)+runID+'.sol','w') as solfile:
		solfile.write(str(int(cost)))
		solfile.write('\n')
		solfile.write(','.join([str(c) for c in tour]))

	print cost, runtime
	return cost,runtime


if __name__ == '__main__':
	main(sys.argv[1:])