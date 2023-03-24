import sys
import dictionary as dict
import pprint
# class Distance_Vector():

# # create infinite variable with largest value possible
inf = sys.maxsize

def distance_vector(graph, src, dest):

    graph_dict = dict.node_string(graph)

    # dictionary of cost and predecessor in each node and 
    # pred will give the path from source node A to pred node
    # cost of each node
    node = dict.node_dict(graph)

    # the cost of first node is 0
    node[src]['cost'] = 0

    for i in range(5):
        # printing iteration number
        #print('Iteration '+str(i)) 
        # iterating over the nodes 
        for itr in graph_dict:          
            #print("Iteration node: " + itr) 
            # accessing neighbor nodes of the current node it's iterating from the dic graph
            for neighbor in graph_dict[itr]: 
                # bellman-ford equation: node[itr]['cost'] - cost of the node, graph[itr][neighbor] - cost of the edge
                # cost = cost of reaching neighbor node
                cost = node[itr]['cost'] + graph_dict[itr][neighbor]
                # comapring costs
                #print(cost)
                #print(node[neighbor]['cost'])
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
        pprint.pprint(node)
    print("Least cost: ", node[dest]['cost'])
    # printing predecessor path
    print("Shortest Path: ", node[dest]['pred'] + list(dest))


if __name__ == "__main__":

    # cost of neighbor edges
    # an example from networkDemo 
    graph = {1: {2: 5}, 
            2: {3: 10, 4: 15}, 
            3: {4: 5}, 
            4: {}
            } 

# Try with different nodes
# ask user for input
# source_node = input("Enter source node: ")
source_node = 1
source = str(source_node)
# dest_node = input("Enter destination node: ")
dest_node = 4
destination = str(dest_node)
distance_vector(graph, source, destination)
