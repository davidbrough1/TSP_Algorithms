from project import CSE6140Project
from approximation import approximation
from simulated_annealing import simulated_annealing


def test():
    project = CSE6140Project()
    project.load_file('/home/david/Desktop/berlin52.tsp')
    print 'Graph Name', project.parameters['name']
    print 'Number of Nodes', project.Graph.number_of_nodes()
    print 'Edge Weight Type', project.parameters['edge_weight_type']
    print 'Number of Edges', project.Graph.number_of_edges(), '\n'
    project.load_file('/home/david/Desktop/burma14.tsp')
    print 'Graph Name', project.parameters['name']
    print 'Edge Weight Type', project.parameters['edge_weight_type']
    print 'Number of Nodes', project.Graph.number_of_nodes()
    print 'Number of Edges', project.Graph.number_of_edges()


def test_approx(file_name):
    project = CSE6140Project()
    project.load_file(file_name)
    opt_cost = float(project.parameters['optimal_cost'])
    solution = approximation(project.Graph, 5, 7)
    print project.parameters['name']
    print opt_cost
    print solution
    print (solution[0] - opt_cost) / opt_cost


def test_simulated_annealing(file_name):
    project = CSE6140Project()
    project.load_file(file_name)
    solution = simulated_annealing(project.Graph, 300, 7)
    opt_cost = float(project.parameters['optimal_cost'])
    print solution
    print (solution[0] - opt_cost) / opt_cost

if __name__ == '__main__':
    file_list = ['burma14.tsp', 'ulysses16.tsp', 'berlin52.tsp',
                 'kroA100.tsp', 'ch150.tsp', 'gr202.tsp']
    for file_name in file_list:
        test_approx(file_name)
        test_simulated_annealing(file_name)
        print ''
