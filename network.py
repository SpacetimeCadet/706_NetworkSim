import copy

class Network():
    def __init__(self, nodes, links):
        self.nodes = nodes # A list of numeric identifiers for the nodes of the network.
        self.links = links # A list of triples in the form [nodeSource, nodeDestination, Weight].

    # THIS METHOD IS NOT YET COMPLETE
    def generateNetwork(self, size):
            self.nodes = []
            self.nodes = [n for n in range(size)]
            self.links = []

            #for i in range(size):
                # randomly assign links between nodes
                # nested loop or linear approach?


    # this method returns the network formatted into a dictionary
    def toDictionary(self):
        dict = {}
        links = copy.deepcopy(self.links)
        for i in self.nodes:
            list = self.specGetLinksOf(i, links)
            connections = {}
            for j in list:
                connections[j[1]] = j[2]
                self.specRemoveLink(j, links)
            dict[i] = connections
        return dict

    # this method returns a list of links containing the specified node.
    def getLinksOf(self, node):
        l = []
        for i in self.links:
            if i[0] == node or i[1] == node: # we only want 0 and 1, since 2 is Weight.
                l.append(i)
        return l
        
    # this method will create a node as long as it is not already in the list.
    # the list is resorted in ascending order.
    def addNode(self, node):
        if not (node in self.nodes):
            self.nodes.append(node)
            self.nodes.sort()

    # this method will delete a node as long as it is found in the list.
    # it will also remove any links containing the node using:
    # getLinksOf() and removeLink()
    def removeNode(self, node):
        if node in self.nodes:
           self.nodes.remove(node)
           removed = self.getLinksOf(node)
           for i in removed:
               self.removeLink(i)
        
    # this method will create a link as long as it is not already in the list
    # todo: check permutations
    def addLink(self, link):
        if not (link in self.links):
            self.links.append(link)

    # this method will delete a link as long as it is found in the list.
    # todo: check permutations
    def removeLink(self, link):
        if link in self.links:
            self.links.remove(link)

    
    # BELOW ARE HELPER FUNCTIONS FOR THE NETWORK CLASS #
    def specGetLinksOf(self, node, links):
        l = []
        for i in links:
            if i[0] == node or i[1] == node: # we only want 0 and 1, since 2 is Weight.
                l.append(i)
        return l
    
    def specRemoveLink(self, link, links):
        if link in links:
            links.remove(link)

        
    
    
