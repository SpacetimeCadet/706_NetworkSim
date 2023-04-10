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
                        self.addLink([i, j, x])

            # Depth First Search 
            for i in self.nodes:    
                visited = [] # Set to keep track of visited nodes of graph.
                graph = self.toDictionary()
                visited = self.dfs(visited, graph, i)
                
                # connect to random unvisited node
                if len(visited) != len(self.nodes):
                    x = random.randint(0, 50)
                    n = random.randint(0, len(self.nodes)-1)
                    while n in visited:
                        n = random.randint(0, len(self.nodes)-1)
                    self.addLink([i, n, x])

    # this method returns the list of nodes visited in a depth first search                   
    def dfs(self, visited, graph, node):
        if node not in visited:
            visited.append(node)
            for neighbour in graph[node]:
                self.dfs(visited, graph, neighbour)
        return visited

    # this method returns the network formatted into a dictionary
    def toDictionary(self):
        dict = {}
        links = copy.deepcopy(self.links)
        for i in self.nodes:
            list = self.scGetLinksOf(i, links)
            connections = {}
            for j in list:
                if j[0] == i:
                    connections[j[1]] = j[2]
                else:
                    connections[j[0]] = j[2]
                #self.scRemoveLink(j, links)
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
            elif i[0] == nodeB and i[1] == nodeA:
                l.append(i)
        if l == []:
            l = [0, 0, 0]
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
            x = link[0]
            y = link[1]
            w = link[2]

            if x > y:
                link = [y, x, w]
                x = link[0]
                y = link[1]
            
            compare = self.getLinkWith(x, y)
            if compare[0] == 0 and compare[1] == 0:
                self.links.append(link)


    # this method will delete a link as long as it is found in the list.
    # todo: check permutations
    def removeLink(self, link):
        if link in self.links:
            self.links.remove(link)


    ### HELPER FUNCTIONS ###
    
    # this method returns the lowest numbered node not in the network
    def assignNode(self):
        x = 0
        assign = len(self.nodes) 
        for i in self.nodes:
            if i != x:
                assign = x
                return assign
            x = x + 1
            assign = x

        if assign < 0:
            assign = 0
        return assign
    
    # this method reinitializes the network
    def clear(self):
        self.nodes = []
        self.links = []
     
    # this method returns a random True or False value
    def flipCoin(self):
        x = random.randint(1, 9)
        if x == 1:
            return True
        return False

    # special usecase: removeNode()
    def scGetLinksOf(self, node, links):
        l = []
        for i in links:
            if i[0] == node or i[1] == node: # we only want 0 and 1, since 2 is Weight.
                l.append(i)
        return l
    
    # special usecase: removeNode()
    def scRemoveLink(self, link, links):
        if link in links:
            links.remove(link)