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


def test_approx():
    project = CSE6140Project()
    project.load_file('ulysses16.tsp')
    opt_cost = float(project.parameters['optimal_cost'])
    solution = approximation(project.Graph)
    print project.parameters['name']
    print solution
    print opt_cost
    print (solution[0] - opt_cost) / opt_cost


def test_simulated_annealing():
    project = CSE6140Project()
    project.load_file('burma14.tsp')
    solution = simulated_annealing(project.Graph)


if __name__ == '__main__':
    test_simulated_annealing()
