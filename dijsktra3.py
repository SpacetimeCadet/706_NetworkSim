from routerNode import *
from heapq import * #allows us to use heap functions in our code e.g., heapify(), heappush(), heappop(), etc. 
from testcode import * #remove later

def Dijsktra(graph, sourceV, destinationV):
    """
    (dict, str, str) -> list
    
    Returns the shortest path from the sourceV vertex to the destinationV
    vertex given a connected graph where adjacent vertices are connected by
    edges with weights. 
    
    Shorted path means the total sum weights from sourceV to destinationV is 
    minimized. 
    
    >>>Dijsktra(graph1, 'A', 'B')
    Answer
    
    >>>Dijsktra(graph2, 'A', 'F')
    Answer
    
    """
    
    infinity = float('inf') #storing the math concept infinity into a variable called 'infinity'
    
    #creating a dictionary to store all the vertices (aka routers) in our network and its associated property values which we will need for this algo
    node_states = {} 
    for vertex in graph:
        node_states[vertex] = routerNode(vertex) #creating a new dictionary where the keys are the vertex/keys from our given graph dictionary and the values are objects of the routerNode class made to rep those keys, which we will change their attributes of throughout this algorithm
        
    """
    we need the source vertex to have the starting cost value as zero, unlike the rest of the nodes which we want their starting costs to be infinity. We have already set all nodes
    to have the default cost of infinity so we have to change that for the source node now
    """
    node_states[sourceV].updateCost(0)  #before the period is the OBJECT associated with the key sourceV in our node_Info dict and after the period is the fn call to change its cost value
    
    #now we will create a list to collect visited nodes that we have determined are in our final route
    visited = []
    
    #will also create a variable to store/we will keep reassigning this variable to the neighbouring node with the minimum cost, which will become our new temp source node
    #we will initiate its value to our actually starting/source node
    next_source = sourceV
    
    
    
    #need to determine the total number of nodes in our graph. We will need this for the next step
    total_nodes = len(graph)
    
    #need to make sure the new source node we choose is not already in the visited list, if it is, we need to choose the next minimum cost node. Otherwise, we will add it to our visted list. Make as a seperate fn to clean up code?
    while next_source != destinationV: # we halt when the greedy algo reaches the destination node specified via the argument destinationV to the fn
        if next_source not in visited:
            visited.append(next_source) #put new vertex into the visited array
            min_heap = []
            heapify(min_heap) #converting our min_heap variable from a list to a min heap data structure
            for j in graph[next_source]: #so we want to check all the neighbouring nodes of 1 of our nodes in our given graph dict. E.g, if next_source is 'A', we want to look at its neighbouring nodes which are in our sample input graph1 graph: 'B' and 'C' so the value of j will be first 'B', then 'C'. 
                if j not in visited: #bc if j is in the visited list, we dont want to consider it for the next source node 
                    cost = node_states[next_source].getCost() + graph[next_source][j] #cost = cost of current source node + weight of edge/distance from current source to neightbouring node j
                    
                    if cost < node_states[j].getCost(): #we only want to replace 'the sortest distance to NodeX' cost for a node, if its smaller than what is already stored for that node
                        node_states[j].updateCost(cost)
                        new_pred = node_states[next_source].getPred() + [next_source] #adding this line so that the next line below is clearer to read. Basically, we want to think about the node we are going to next and figure out what its sortest path is. Its shortest past, will be the shortest path to the node that comes before it (which is our current source node called, next_source) plus we need to add that source node. We use [] around the last term of that line because next_source is just a node but we need it be a list so that we can concatenate it/add it to that shortest path list for that previous node. 
                        node_states[j].updatePred(new_pred)
                    print(node_states[j]) #for debugging
                        
                    heappush(min_heap, (node_states[j].getCost(), j)) #NOTE: heappush() pushes an element into the heap BUT importantly ensures the min heap property is maintained (by default)! We push it 2 values: 1. the cost of the neighbouring node (all neighbours inside the line 53 for loop) and 2. the name of the neighbouring node
                    
                    #print(min_heap) #for debugging
        ## below code added for the scenario when the greedy choose leads to a dead end/sink node and therefore cannot get to the destination node from the greedy chose taken. 
        if len(min_heap) == 0 and next_source != destinationV:
            next_source = visited[-2]#return to the previous node (which is not our current source node) in our visisted list. visited[-1] would make the current node our next_source node, which is NOT what we want. we would then get stuck in an infinite loop of visiting the same node.
            visited.remove(visited[-2])
            print("We are backtracking to node ", next_source) #for debugging
        else:         
        ##---- above code added for that scenario ending       
            next_source = min_heap[0][1] #now outside of the loop visiting all neighbour nodes (line 55), we want to reassign our current source node (aka next_source) to be the neighbouring node with the least cost, which will be the root node of the min heap data structure. 
            print("Next source node is ", next_source, "\n") #for debugging
                
    print("The shorest path from ", sourceV, " to ", destinationV, " is ", node_states[destinationV].getPred() + [destinationV])
    print("The distance from ", sourceV, " to ", destinationV, " is ", node_states[destinationV].getCost())
    print("What is being returned", node_states[destinationV].getPred() + [destinationV])
    return(node_states[destinationV].getPred() + [destinationV])
            
            
            

#Dijsktra(networkGraph1,'A', 'F') #should return ['A', 'C', 'E', 'F']
#Dijsktra(networkGraph1,'C', 'A') #should return ['C', 'A']
#Dijsktra({'A': {'B':2}, 'B': {'A': 2}},'B', 'A') #should return ['B', 'A']
#Dijsktra(networkGraph2, 'A', 'E')
#networkGraph5 = {
    #'1': {'2':2, '3':4},
    #'2': {'1':2, '3':3, '4':8},
    #'3': {'1':4, '2':3, '5':5, '4':2},
    #'4': {'2':8, '3':2, '5':11, '6': 22},
    #'5': {'3':5, '4':11, '6':1},
    #'6': {'4':22, '5':1}
#}
#Dijsktra(networkGraph5, '1', '6')

#networkGraph3 = {
    #1: {2:2, 3:4},
    #2: {1:2, 3:3, 4:8},
    #3: {1:4, 2:3, 5:5, 4:2},
    #4: {2:8, 3:2, 5:11, 6: 22},
    #5: {3:5, 4:11, 6:1},
    #6: {4:22, 5:1}
#}
#Dijsktra(networkGraph3, 1, 6)


