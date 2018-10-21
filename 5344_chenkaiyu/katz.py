from igraph import *
import os
import random
from random import shuffle
from random import seed

try:
    # Python 2
    xrange
except NameError:
    # Python 3, xrange is now named range
    xrange = range


# Convert edge_list into a set of constituent edges
def get_vertices_set(edge_list):
    res = set()
    for x,y in edge_list:
        res.add(x)
        res.add(y)
    return res


# Calculates the Katz Similarity measure for a node pair (i,j)
def katz_similarity(katzDict,i,j):
    l = 1
    neighbors = katzDict[i]
    score = 0

    # prepare the first round of middle mans
    firstMiddleMan = []
    for k in neighbors:
        firstMiddleMan += katzDict[k]
    neighbors = firstMiddleMan

    while l <= maxl:
        numberOfPaths = neighbors.count(j)
        if numberOfPaths > 0:
            score += (beta**l)*numberOfPaths

        neighborsForNextLoop = []
        for k in neighbors:
            neighborsForNextLoop += katzDict[k]
        neighbors = neighborsForNextLoop
        l += 1

    return score
# Calculates accuracy metrics (Precision & Recall),
# for a given similarity-model against a test-graph.
def print_precision_and_recall(sim,train_graph,test_graph,test_vertices_set,train_vertices_set):
    precision = recall = c = 0
    for i in test_vertices_set:
        if i in train_vertices_set:
            actual_friends_of_i = set(test_graph.neighbors(i))

            # Handles case where test-data < k
            if len(actual_friends_of_i) < k:
                k2 = len(actual_friends_of_i)
            else:
                k2 = k

            top_k = set(get_top_k_recommendations(train_graph,sim,i,k2))

            precision += len(top_k.intersection(actual_friends_of_i))/float(k2)
            recall += len(top_k.intersection(actual_friends_of_i))/float(len(actual_friends_of_i))
            c += 1
    print("Precision is : " + str(precision/c))
    print("Recall is : " + str(recall/c))

def split_data(edge_list):
    random.seed(350)
    indexes = range(len(list(edge_list)))
    test_indexes = set(random.sample(indexes, len(indexes)/2)) # removing 50% edges from test data
    train_indexes = set(indexes).difference(test_indexes)
    test_list = [edge_list[i] for i in test_indexes]
    train_list = [edge_list[i] for i in train_indexes]
    return train_list,test_list

beta = 0.1  # The damping factor for Katz Algorithm
maxl = 2    # Number of iterations for Katz Algorithm (beta^maxl ~ 0)

data_file = open('./test_0/train_set_0.txt')
edge_list = map(lambda x:tuple(map(int,x.split())),data_file.read().split("\n")[:])
train_list = list(edge_list)

train_set = set(train_list)
train_graph = Graph(train_list)
train_n =  train_graph.vcount()

# def katz(train_list, train_graph, train_n, train_set):
#     train_vertices_set = get_vertices_set(train_list) # Need this because we have to only consider target users who are present in this train_vertices_set

#     # build a special dict that is like an adjacency list
#     katzAdjDict = {}
#     katz_dict = {}
#     adjList = train_graph.get_adjlist()

    # for i, l in enumerate(adjList):
    #     katzAdjDict[i] = l


    # for i in xrange(train_n):
    #     print(i)

    #     for j in xrange(i+1, train_n):
    #         if (i,j) not in train_set: # eliminate the chances that two persons are already friends
    #             katz_dict[str(i) + '_' + str(j)] = katz_dict[str(j) + '_' + str(i)] = katz_similarity(katzAdjDict,i,j)


    # return katz_dict

def getPathsMap(train_list, train_graph, train_n): 
    print (train_n)
    train_set = set(train_list) 

    # init preparation
    pathsMap = [ [ [0] * 3 for _ in range(train_n)] for _ in range(train_n)]


    print("preparation starts")
    # for direct linking
    for i in range(train_n):
        for j in train_graph.neighbors(i):
            if (i, j) in train_set:
                pathsMap[i][j][0] = pathsMap[j][i][0] = 1


    print ("preparation done")


    # for nodes needs a middle man to connect together
    for i in range(train_n):
        for j in range(i + 1, train_n):
            if pathsMap[i][j][0] == 0: 
                for k in train_graph.neighbors(i):
                    if pathsMap[k][j][0] > 0:
                        result = pathsMap[i][j][1] + pathsMap[i][k][0]
                        pathsMap[i][j][1] = pathsMap[j][i][1] = result

    print ("first middle man done")

    # for nodes needs two middle man
    for i in range(train_n):
        for j in range(i + 1, train_n):
            if pathsMap[i][j][0] == 0:
                for k in train_graph.neighbors(j):
                    if pathsMap[i][k][1] > 0:
                        result = pathsMap[i][j][2] + pathsMap[i][k][1]
                        pathsMap[i][j][2] = pathsMap[j][i][2] = result

    print ("second middle man done")

    return pathsMap


def katz(pathsMap, train_n): 
    katz_dict = {}

    print("katz starts")
    for i in range(train_n):
        print(i)
        for j in range(i+1, train_n):
            if pathsMap[i][j][0] == 0: # exclude the direct pathsMap
                katz_dict[str(i) + '_' + str(j)] = katz_dict[str(j) + '_' + str(i)] = beta * pathsMap[i][j][1] + beta**2 * pathsMap[i][j][2]
    
    
    print ("katz done")
    return katz_dict
pathsMap = getPathsMap(train_list, train_graph, train_n)
        
katz_dict = katz(pathsMap, train_n)
katz_dict = sorted(katz_dict.items(),key = lambda x:x[1],reverse = True) 

with open('./test_0/katz_output.txt', 'w',encoding='UTF-8') as f:
    for key in katz_dict: 
        fromV = key[0].split('_')[0]
        toV = key[0].split('_')[1]
        if fromV < toV: 
            f.write(fromV + ' ' + toV + ' ' + str(key[1]) + '\n')
f.close
# print_precision_and_recall(sim,train_graph,test_graph,test_vertices_set,train_vertices_set)