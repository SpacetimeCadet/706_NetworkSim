import copy, random

class Network():
    def __init__(self, nodes, links):
        self.nodes = nodes # A list of numeric identifiers for the nodes of the network.
        self.links = links # A list of triples in the form [nodeSource, nodeDestination, Weight].


    # this method clears the current network and randomly generates a network of the specified size (must be between 2-20 nodes)
    def randomizeNetwork(self, size):
            # Initialize Network and Verify Arguments
            self.clear()
            if size > 20:
                i = 20
            elif size < 2:
                i = 2
            else:
                i = size

            # Generate Nodes
            self.nodes = [n for n in range(i)]

            # Generate Links
            for i in self.nodes:
                for j in self.nodes:
                    if i != j and self.flipCoin():
                        x = random.randint(0, 50)
                        self.links.append([i, j, x])


    # this method returns the network formatted into a dictionary
    def toDictionary(self):
        dict = {}
        links = copy.deepcopy(self.links)
        for i in self.nodes:
            list = self.scGetLinksOf(i, links)
            connections = {}
            for j in list:
                connections[j[1]] = j[2]
                self.scRemoveLink(j, links)
            dict[i] = connections
        return dict
    

    # this method returns the weight of the link between the specified nodes.
    def getWeight(self, nodeA, nodeB):
        link = self.getLinkWith(nodeA, nodeB)
        return link[0][2]
    

    # this method will update the weight of a link as long as it is found in the list.
    def setWeight(self, nodeA, nodeB, weight):
        link = self.getLinkWith(nodeA, nodeB)
        link = link[0]
        if link in self.links:
            src = link[0]
            dst = link[1]
            i = self.links.index(link)
            self.links[i] = [src, dst, weight]


    # this method returns a list of links containing the specified node.
    def getLinksOf(self, node):
        l = []
        for i in self.links:
            if i[0] == node or i[1] == node: # we only want 0 and 1, since 2 is Weight.
                l.append(i)
        return l
    

    # this method returns a link (as a list) containing the specified nodes
    def getLinkWith(self, nodeA, nodeB):
        l = []
        for i in self.links:
            if i[0] == nodeA and i[1] == nodeB:
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
    def addLink(self, link):
        #TODO: permutations (different order, same weights) 
        #          and duplicates (either order, different weights)
        
        if not (link in self.links):
            if link[0] < link[1]:
                x = link[0]
                y = link[1]
                w = link[2]
                link = [y, x, w]
                print(x,y,w)
                print(link)
            self.links.append(link)


    # this method will delete a link as long as it is found in the list.
    # todo: check permutations
    def removeLink(self, link):
        if link in self.links:
            self.links.remove(link)


    ### HELPER FUNCTIONS ###
    def scGetLinksOf(self, node, links):
        l = []
        for i in links:
            if i[0] == node or i[1] == node: # we only want 0 and 1, since 2 is Weight.
                l.append(i)
        return l
    

    def scRemoveLink(self, link, links):
        if link in links:
            links.remove(link)


    # this method returns a random True or False value
    def flipCoin(self):
        x = random.randint(1, 10)
        if x == 1:
            return True
        return False


    def assignNode(self):
        x = 1
        assign = len(self.nodes) 
        for i in self.nodes:
            if i != x:
                assign = x
                return assign
            x = x + 1
            assign = x

        if assign < 1:
            assign = 1
        return assign
    
    def clear(self):
        self.nodes = []
        self.links = []