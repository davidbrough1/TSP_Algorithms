#This file is used to test the code.
import subprocess


def test(filename, method, cutoff, seed):
    commandline = ['python', 'TSP.py', '--inst', filename, '--alg',
                   method, '--time', str(cutoff), '--seed', str(seed)]
    subprocess.call(commandline)

if __name__ == '__main__':
    file_list = ['burma14.tsp', 'ulysses16.tsp', 'berlin52.tsp',
                 'kroA100.tsp', 'ch150.tsp', 'gr202.tsp']
    seed_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    methods = ['LS2', 'Approx']
    for file_name in file_list:
        for seed in seed_list:
            for method in methods:
                test(file_name, method, 600, seed)
