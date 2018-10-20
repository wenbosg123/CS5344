
# coding: utf-8

# In[3]:


from igraph import *
import time

print(int(time.time()))
data_file = open('./test_0/train_set_0.txt')
edge_list = map(lambda x:tuple(map(int,x.split())),data_file.read().split("\n")[:-1])
train_list = list(edge_list)
train_set = set(train_list)
train_graph = Graph(train_list)
train_n =  train_graph.vcount()

nodes= set()
for x,y in train_list:
    nodes.add(x)
    nodes.add(y)

cn_dict = {}
jaccard_dict = {}
adamic_adar_dict = {}
preferential_attachment_dict = {}
for i in range(train_n):
        for j in range(i,train_n):
            if i!=j and i in nodes and j in nodes:
                if (i,j) not in train_set:
                    cn_dict[str(i) + '_' + str(j)] = len(set(train_graph.neighbors(i)).intersection(set(train_graph.neighbors(j))))
                    
                    union_nodes = len(set(train_graph.neighbors(i)).union(set(train_graph.neighbors(j))))
                    if union_nodes != 1:
                        jaccard_dict[str(i) + '_' + str(j)] = len(set(train_graph.neighbors(i)).intersection(set(train_graph.neighbors(j))))/float(union_nodes)
                    
                    adamic_adar_dict[str(i) + '_' + str(j)] = sum([1.0/math.log(train_graph.degree(v)) for v in set(train_graph.neighbors(i)).intersection(set(train_graph.neighbors(j)))])
                    
                    preferential_attachment_dict[str(i) + '_' + str(j)] = train_graph.degree(i) * train_graph.degree(j)
cn_dict = sorted(cn_dict.items(),key = lambda x:x[1],reverse = True)
jaccard_dict = sorted(jaccard_dict.items(),key = lambda x:x[1],reverse = True)
adamic_adar_dict = sorted(adamic_adar_dict.items(),key = lambda x:x[1],reverse = True)
preferential_attachment_dict = sorted(preferential_attachment_dict.items(),key = lambda x:x[1],reverse = True)

with open('./test_0/cn_output.txt', 'w',encoding='UTF-8') as f:
    for key in cn_dict:
        f.write(key[0].split('_')[0] + ' ' + key[0].split('_')[1] + ' ' + str(key[1]) + '\n')
f.close

with open('./test_0/jaccard_output.txt', 'w',encoding='UTF-8') as f:
    for key in jaccard_dict:
        f.write(key[0].split('_')[0] + ' ' + key[0].split('_')[1] + ' ' + str(key[1]) + '\n')
f.close

with open('./test_0/adamic_adar_output.txt', 'w',encoding='UTF-8') as f:
    for key in adamic_adar_dict:
        f.write(key[0].split('_')[0] + ' ' + key[0].split('_')[1] + ' ' + str(key[1]) + '\n')
f.close

with open('./test_0/preferential_attachment_output.txt', 'w',encoding='UTF-8') as f:
    for key in preferential_attachment_dict:
        f.write(key[0].split('_')[0] + ' ' + key[0].split('_')[1] + ' ' + str(key[1]) + '\n')
f.close

print(int(time.time()))

