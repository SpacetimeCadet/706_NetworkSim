from network import Network

# generateNetwork() is still under development

# ex. instantiate manually
# n = Network([nodes], [links]); where links are [source, destination, weight]
n = Network([1, 2, 3, 4], [[1, 2, 5], [2, 3, 10], [2, 4, 15], [3, 4, 5]])

print("- - - - -")
print("Initial State")
print(n.nodes)
print(n.links)
print("- - - - -")

print("Links Containing Node #2")
print(n.getLinksOf(2)) # the list of links containing node #2
print("- - - - -")

print("Add Node #7")
n.addNode(7) # new node is added.
print(n.nodes)
print(n.links)
print("- - - - -")

print("Add Node #5")
n.addNode(5) # the list is sorted after new nodes are added.
print(n.nodes)
print(n.links)
print("- - - - -")

print("Remove Node #2")
n.removeNode(2) # removing a node will also remove any links containing it.
print(n.nodes)
print(n.links)
print("- - - - -")