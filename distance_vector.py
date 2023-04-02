import dictionary as d
import pprint


# create infinite variable with largest value possible
inf = float('inf')

def dist_vec(graph, source, destination):

    graph_dict = d.node_string(graph)
    src = str(source)
    dest = str(destination)

    '''dictionary of cost and predecessor in each node and 
       pred will give the path from source node A to pred node
       cost of each node'''
    node_data = d.node_dict(graph)

    # the cost of first node is 0
    node_data[src]['cost'] = 0

    cost_node = []
    distance = []

    for i in range(len(graph_dict) - 1):
        # printing iteration number
        # print('Iteration '+str(i)) 
        # iterating over the nodes 
        for itr in graph_dict:          
            #print("Iteration node: " + itr) 
            # accessing neighbor nodes of the current node it's iterating from the dic graph
            for neighbor in graph_dict[itr]: 
                '''bellman-ford equation: node[itr]['cost'] - cost of the node, graph[itr][neighbor] - cost of the edge
                    cost = cost of reaching neighbor node
                    node_data[itr]['cost']: cost of a node
                    graph_dict[itr][neighbor]: cost of an edge, e.g. A-->B: 6'''
                cost = node_data[itr]['cost'] + graph_dict[itr][neighbor] 
                # comapring costs, if the new cost is less than the node's present cost
                if cost < node_data[neighbor]['cost']:
                    node_data[neighbor]['cost'] = cost
                    '''gives predecessor nodes that are used to reach a destination node
                    if inf then the node wasn't explored'''
                    if node_data[neighbor]['cost'] == inf:
                        # update the predecessor nodes list of the itr nodes
                        node_data[neighbor]['pred'] = node_data[itr]['pred'] + list(itr)
                    else:
                        # clears the previous cost if smaller cost is found
                        node_data[neighbor]['pred'].clear()
                        node_data[neighbor]['pred'] = node_data[itr]['pred'] + list(itr)     
      
        # print("Iteration:", str(i))    
        # pprint.pprint(node_data)

    # detecting negative cycle
    # after (number of nodes - 1) iterations 
    # if the cost of any nodes changes (lesser cost) then there is a negative cycle
    # for itr in graph_dict:
    #     for neighbour in graph_dict[itr]:
    #         if (node_data[itr]['cost'] + graph_dict[itr][neighbour] < node_data[neighbour]['cost'] and cost != inf):
    #             print("Negative cycle detected") 
    #             return

    least_cost = node_data[dest]['cost']
    #print("Least Cost: " ,least_cost)
    path_node_s = node_data[dest]['pred'] + list(dest)    
    path_node = [eval(i) for i in path_node_s]
    #print(path_node)
    # pprint.pprint(node_data)
    # print("Least cost",least_cost)
    # print("Nodes used in the path: " , path_node)
    # print("Shortest path: ", shortest_path)

    # returning the shortest path as a list
    # list is in a form of [source node, dest node, cost]
    shortest_path = []
    for itr in range(len(path_node)-1):
        for i in graph:
            for j in graph[i]:
                if (i==path_node[itr] and j==path_node[itr+1]):
                    shortest_path.append([i,j,graph[i][j]])
                break 
    return shortest_path


# if __name__ == "__main__":

#     # cost of neighbor edges
#     # an example from networkDemo 
#     graph = {
#             0: {1: 6, 2: 4, 3: 5}, 
#             1: {4: 1}, 
#             2: {1: 2, 4: 3}, 
#             3: {2: 2, 5: 1}, 
#             4: {5: 3}, 
#             5: {}
#             }

# # Try with different nodes
# # ask user for input
# # source_node = input("Enter source node: ")
# source = 0
# # dest_node = input("Enter destination node: ")
# destination = 4
# g = dist_vec(graph, source, destination)
# print(g)

