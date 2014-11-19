import networkx as nx
import math


class CSE6140Project(object):

    def __init__(self):
        '''
        Initialize an instance of CSE6140Project.
        '''
        self.parameters = {}
        self.Graph = None
        self.time_cutoff = None

    def load_file(self, file_path):
        '''
        Loads a file and generates the parameters dictionary and a graph.
        '''
        f = open(file_path, 'r')
        file_data = f.readlines()
        self.parameters['name'] = file_data[0][6:].rstrip()
        self.parameters['comments'] = file_data[1][9:].rstrip()
        self.parameters['dimensions'] = file_data[2][11:].rstrip()
        self.parameters['edge_weight_type'] = file_data[3][18:].rstrip()
        self.parameters['optimal_cost'] = file_data[4][14:].rstrip()
        self.parameters['header'] = file_data[5].rstrip()
        node_locations = file_data[6:6 + int(self.parameters['dimensions'])]
        edge_weights = self._get_weights(node_locations,
                                         self.parameters['edge_weight_type'])
        G = nx.Graph()
        G.add_weighted_edges_from(edge_weights)
        self.Graph = G

    def _get_weights(self, node_locations, edge_weight_type):
        '''
        Helper function to get edge weights.
        '''
        tuple_node_locations = [(int(x.split()[0]), float(x.split()[1]),
                                 float(x.split()[2])) for x in node_locations]
        if edge_weight_type[:3] == 'GEO':
            weights = self._get_geo_weights(tuple_node_locations)
        else:
            weights = self._get_euclidean_weights(tuple_node_locations)
        return weights

    def _get_geo_weights(self, tuple_node_locaitons):
        '''
        Helper function to calculated weights from geo coordinates.
        '''
        edge_weights = []
        earth_r = 6371
        for node_i in tuple_node_locaitons:
            for node_j in tuple_node_locaitons:
                if node_j[0] > node_i[0]:
                    del_phi = (node_j[1] - node_j[1]) * math.pi / 180
                    del_lambda = (node_j[2] - node_i[2]) * math.pi / 180
                    phi_1 = node_j[1] * math.pi / 180
                    phi_2 = node_i[1] * math.pi / 180
                    a = math.sin(del_phi / 2) ** 2 + math.cos(phi_1) * \
                        math.cos(phi_2) * math.sin(del_lambda / 2) ** 2
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                    weight = earth_r * c
                    edge_weights.append((node_j[0], node_i[0], weight))
        return edge_weights

    def _get_euclidean_weights(self, tuple_node_locaitons):
        '''
        Helper function to calculate weights from using euclidean distance.
        '''
        edge_weights = []
        for node_i in tuple_node_locaitons:
            for node_j in tuple_node_locaitons:
                if node_j[0] > node_i[0]:
                    weight = math.sqrt((node_j[1] - node_i[1]) ** 2 +
                                       (node_j[2] - node_i[2]) ** 2)
                    edge_weights.append((node_i[0], node_j[0], weight))
        return edge_weights



