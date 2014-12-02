import sys
from genetic_algorithm import *
from timeout import timeout

@timeout(int(sys.argv[2]))
def main(args):
	filename = args[0]
	cutoff_time = float(args[1])
	method = args[2]
	random_seed = args[3]
	
	if method == 'GA':
		run_genetic_algorithm(filename,random_seed)
	elif method == 'BnB':
		pass
	elif method == 'Greedy':
		pass
	elif method == 'SA':
		pass
	elif method == 'Approx':
		pass
	else:
		print "Incorrect Method Entered. The correct options are:\nGA, BnB, Greedy, SA, Approx"

if __name__ == '__main__':
	main(sys.argv[1:])

