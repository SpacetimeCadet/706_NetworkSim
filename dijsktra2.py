from routerNode import *

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
        node_states[vertex] = routerNode #creating a new dictionary where the keys are the vertex/keys from our given graph dictionary and the values are objects of the routerNode class made to rep those keys, which we will change their attributes of throughout this algorithm
        
    """
    we need the source vertex to have the starting cost value as zero, unlike the rest of the nodes which we want their starting costs to be infinity. We have already set all nodes
    to have the default cost of infinity so we have to change that for the source node now
    """
    node_states[sourceV].updateCost(0)  #before the period is the OBJECT associated with the key sourceV in our node_Info dict and after the period is the fn call to change its cost value
    
    #now we will create a list to collected visited nodes that we have determined are in our final route
    visited = []
    
    #will also create a variable to store/we will keep reassigning this variable to the neighbouring node with the minimum cost, which will be come our new temp source node
    #we will initiate its value to our actually starting/source node
    next_source = sourceV
    
    
    
    #need to determine the total number of nodes in our graph. We will need this for the next step
    total_nodes = len(graph)
    
    #need to make sure the new source node we choose is not already in the visited list, if it is, we need to choose the next minimum cost node. Otherwise, we will add it to our visted list. Make as a seperate fn to clean up code?
    for i in range(total_nodes - 1): # minus 1 because range starts at zero, not 1. so to iterate total_Nodes times, we need to write total_nodes minus 1
        if next_source not in visited:
            visited.append(next_source) 
            temp = []
            if j in graph[next_source]: #so we want to check all the neighbouring nodes of 1 of our nodes in our given graph dict. E.g, if next_source is 'A', we want to look at its neighbouring nodes which are in our sample input graph1 graph: 'B' and 'C' so the value of j will be first 'B', then 'C'. 
                if j not in visited: #bc if j is in the visited list, we dont want to consider it for the next source node 
                    cost = node_states[next_source].getCost() + graph[next_source][j] #cost = cost of current source node + weight of edge from current course to neightbouring node j
                    
                    if cost < node_states[j].getCost(): #we only to replace 'the sortest distance from A' cost for a node, if its smaller than what is already stored for that node
                        node_states[j].updateCost(cost)
                        new_pred = node_states[next_source].getPred() + list(next_source)  #adding this line so that the next line below clearer to read. Basically, we want to think about the node we are going to next and figure out what its sortest path is. Its shortest past, will be the shortest path to the node that comes before it (which is our current source node called, next_source) plus we need to add that source node. We use the list() fn for the last term of that line because next_source is just a node but we need it be a list so that we can concatenate it/add it to that shortest path list for that previous node. 
                        node_states[j].updatePred(new_pred)
                        
                    min = temp[0][0] # creating a variable to find the minimum cost. ?? What to do if no neighbouring nodes?
                    temp.append((node_states[j].getCost(), j))  #put all the neighbouring nodes into a list via a tuple of the neighbour cost and its node name
                    ##print(temp)
                    for cost in temp:
                    
                    
                        
                        
                        
                        
                        
                        
                        
       
                        
                        
                    
    
    
