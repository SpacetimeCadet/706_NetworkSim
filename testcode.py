#Ex/ Test Code:

networkGraph1 = {
    'A': {'B':2, 'C':4},
    'B': {'A':2, 'C':3, 'D':8},
    'C': {'A':4, 'B':3, 'E':5, 'D':2},
    'D': {'B':8, 'C':2, 'E':11, 'F': 22},
    'E': {'C':5, 'D':11, 'F':1},
    'F': {'D':22, 'E':1}
}
"""
graph above was found from online. 

uses a dictionary to store the graph where:

Keys = the vertices of the graph

Values = another diction where the inner key = a neighbouring vertex and its 
associated value is its cost to get from the outter key to that neighbouring key
(aka the edge value to get to that inner key from the outter key)

"""
networkGraph2 = {
    'A': {'B':2, 'C':4},
    'B': {'A':2, 'C':3, 'D':8},
    'C': {'A':4, 'B':3},
    'D': {'B':8,'E': 22},
    'E': {'D':22}
}
"""
Above graph was created to test an edge case. We still need to find the shortest
path even if the greedy choose at one node leads to an sink node that is NOT 
our destination node. 

In this case, that sink node is node C. The algo must back track its greedy choose
to still make it to the destination node. 
"""