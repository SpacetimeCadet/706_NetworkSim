
import sys

inf = sys.maxsize

# function for converting integer nodes to string
def node_string(graph):
    keys = {}
    values = []

    for k, v in graph.items():
        str1 = str(k)
        keys[str1] = {}
        values.append(v)

    klist = []
    vlist = []
    for i in values:
        key_list = list(i)
        list_string = map(str, key_list)
        val_list = list(i.values())
        klist.append(list(list_string))
        vlist.append(val_list)

    res = []
    for i in range(len(klist)):
        l1 = klist[i]
        l2 = vlist[i]
        res_dict = dict(zip(l1,l2))
        res.append(res_dict)
  
    d = {}
    for k, v in keys.items():
        index = list(keys.keys()).index(k)
        d[k] = res[index]

    return d
    
# function to create a node dictionary that initializes starting cost as infinity
def node_dict(graph):
    key ={}
    for k, v in graph.items():
        s = str(k)
        key[s] = {'cost':inf,'pred':[]}
    return key
    
# if __name__ == '__main__':
        
#         # this graph isn't changing 
#         graph =  {
#         1:{2:6,3:4,4:5},
#         2:{5:-1},
#         3:{2:-2,5:3},
#         4:{3:-2,6:-1},
#         5:{6:3},
#         6:{}
#     }

# #node_string(graph)
# g = node_dict(graph)
# d = node_string(graph)
# print(d)
# print(g)





    



    

    
    

