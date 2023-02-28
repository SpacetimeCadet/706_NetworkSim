class Network():
    def __init__(self, nodes, links):
        self.nodes = nodes
        self.links = links

    def getNodeList(self):
        return self.nodes
    
    def getLinkList(self):
        return self.links
    
    def getLinksOf(self, node):
        l = []
        for i in self.links:
            if i[0] == node or i[1] == node:
                l.append(i)
        return l

        
    
    
