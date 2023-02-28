class Network():
    def __init__(self, nodes, links, weights):
        self.nodes = nodes
        self.links = links
        self.weights = weights

    def getNodeList(self):
        return self.nodes