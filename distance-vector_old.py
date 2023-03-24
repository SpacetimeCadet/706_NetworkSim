import sys
import main as m
import network as n

# finds the shortest distance from the source node 
# to all of the nodes until reaches the destination 
# dynamic programming <-- store results of sub problems

# Bellman-form equation (adjustment): 
# if: cost(source node) + weight-of-edge < cost(dest)
#               |                    |        |
#               |                    |     (cost from specific source to destination)
#     (cost of reaching source node) |
#                           (cost of reaching the destination node)
# then: cost(dest) = cost(source node) + weight-of-edge
# apply adjustment for all the edges of the graph

class Distance_Vector():

    # a function is needed to that outputs a dict of 

    def distance_vector(graph, src, dest):

        # create infinite variable
        inf = sys.maxsize

        # dictionary of cost and predecessor in each node and 
        # pred will give the path from source node A to pred node

        # cost of each node
        node = {1:{'cost':inf,'pred':[]},
            2:{'cost':inf,'pred':[]},
            3:{'cost':inf,'pred':[]},
            4:{'cost':inf,'pred':[]},
            5:{'cost':inf,'pred':[]},
            6:{'cost':inf,'pred':[]}
        }

        # the cost of first node is 0
        node[src]['cost'] = 0

        for i in range(5):
            # printing iteration number
            print('Iteration '+str(i)) 
            # iterating over the nodes e.g. A,B,C...
            for itr in graph:          
                #print("Iteration node: " + itr) 
                # accessing neighbor nodes of the current node it's iterating from the dic graph
                for neighbor in graph[itr]: 
                    # bellman-ford equation: node[itr]['cost'] - cost of the node, graph[itr][neighbor] - cost of the edge
                    # cost = cost of reaching neighbor node
                    cost = node[itr]['cost'] + graph[itr][neighbor]
                    # comapring costs
                    if cost < node[neighbor]['cost']:
                        node[neighbor]['cost'] = cost
                        # gives predecessor nodes that are used to reach a destination node
                        # if inf then the node wasn't explored
                        if node[neighbor]['cost'] == inf:
                            # update the predecessor nodes list of the itr nodes
                            node[neighbor]['pred'] = node[itr]['pred'] + list(itr)
                        else:
                            # clears the previous cost if smaller cost is found
                            node[itr]['pred'].clear()
                            node[neighbor]['pred'] = node[itr]['pred'] + list(itr)
            print(node)
        print("Shortest Distance: "+ str(node[dest]['cost']))
        # printing predecessor path
        print("Shortest Path: "+ str(node[dest]['pred'] + list(dest)))


    if __name__ == "__main__":

        # cost of neighbor edges
        # an example
        graph = {
            1:{2:6,3:4,4:5},
            2:{5:-1},
            3:{2:-2,5:3},
            4:{3:-2,6:-1},
            5:{6:3},
            6:{}
        }

    # Try with different nodes
    source = 1
    destination = 5
    distance_vector(graph, source, destination)
