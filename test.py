from network import Network

n = Network([1, 2, 3, 4], [[1, 2, 5], [2, 3, 10], [2, 4, 15], [3, 4, 5]])

print(n.getLinksOf(2))