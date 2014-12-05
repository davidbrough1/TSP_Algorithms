#This file contains a helper function used by the branch and bound algorithm.

def computeBound(self):
    '''
    Returns a lowerbound on the optimal tour for this node
    '''
    # Use getAt to find distance between nodes
    # Sum of shortest individual paths from each node
    shortest = 0
    for name1 in self.state.nodeNames:
        short = -1
        if name1 not in self.path:
            for name2 in self.state.nodeNames:
                if name2 not in self.path and name1 != name2:
                    if short == -1 or self.state.get_dist(name1, name2) < short:
                        short = self.state.get_dist(name1, name2)
        if short:
            shortest += short
    return (shortest + self.pathLength)
