import sys
from genetic_algorithm import *
from greedy import *
from timeout import timeout
from approximation import approximation
from simulated_annealing import run_simulated_annealing

#@timeout(int(sys.argv[2]))


@timeout(100000)
def main(args):
    filename = args[0]
    cutoff_time = int(args[1])
    method = args[2]
    random_seed = args[3]
    print 'filename', filename
    print 'cutoff_time', cutoff_time
    print 'method', method
    print 'random_seed', random_seed

    if method == 'LS1':
        runID = '_' + str(random_seed)
        tour, cost, runtime = run_genetic_algorithm(
            filename, method, random_seed, cutoff_time, runID)
    elif method == 'BnB':
        runID = ''
    elif method == 'Heuristic':
        tour, cost = run_greedy_algorithm(filename, random_seed)
        runID = ''
    elif method == 'LS2':
        tour, cost, runtime, trace = run_simulated_annealing(filename,
                                                             random_seed)
        runID = '_' + str(random_seed)
        _make_trace_file(filename, method, cutoff_time, runID, trace)
    elif method == 'Approx':
        tour, cost, runtime = approximation(filename, random_seed)
        runID = '' + str(random_seed)
    else:
        print "Incorrect Method Entered. The correct options are:\n" + \
            "GA, BnB, Greedy, SA, Approx"

    # for runID in xrange(1,11):
    with open('op/' + filename[:-4] + '_' + method + '_' +
              str(cutoff_time) + runID + '.sol', 'w') as solfile:
        solfile.write(str(int(cost)))
        solfile.write('\n')
        solfile.write(','.join([str(c) for c in tour]))

    return cost, runtime


def _make_trace_file(filename, method, cutoff_time, runID, tracelist):
    with open(filename + '_' + method + '_' + cutoff_time
              + '_' + runID + '.trace', 'w') as tracefile:
        for trace in tracelist:
            tracefile.write(str(trace)[1:-1])


if __name__ == '__main__':
    main(sys.argv[1:])
    # main(['burma14.tsp', '20', 'LS2', '3'])
