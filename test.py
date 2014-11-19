from project import CSE6140Project


def test():
    project = CSE6140Project()
    project.load_file('berlin52.tsp')
    print 'Graph Name', project.parameters['name']
    print 'Number of Nodes', project.Graph.number_of_nodes()
    print 'Edge Weight Type', project.parameters['edge_weight_type']
    print 'Number of Edges', project.Graph.number_of_edges(), '\n'
    project.load_file('burma14.tsp')
    print 'Graph Name', project.parameters['name']
    print 'Edge Weight Type', project.parameters['edge_weight_type']
    print 'Number of Nodes', project.Graph.number_of_nodes()
    print 'Number of Edges', project.Graph.number_of_edges()

if __name__ == '__main__':
    test()
