from network import Network

# generateNetwork() is still under development

# ex. instantiate manually
n = Network([1, 2, 3, 4], [[1, 2, 5], [2, 3, 10], [2, 4, 15], [3, 4, 5]])

print("- - - - -")
print(n.nodes)
print(n.links)
print(n.getLinksOf(2)) # the list of links containing node #2

print("- - - - -")
print(n.nodes)
print(n.links)
n.addNode(7) # new node is added.

print("- - - - -")
print(n.nodes)
print(n.links)
n.addNode(5) # the list is sorted after new nodes are added.

print("- - - - -")
print(n.nodes)
print(n.links)
n.removeNode(2) # removing a node will also remove any links containing it.

print("- - - - -")
print(n.nodes)
print(n.links)