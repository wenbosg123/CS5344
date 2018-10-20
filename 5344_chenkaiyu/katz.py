from igraph import *

data_file = open('./test_0/train_set_0.txt')
edge_list = map(lambda x:tuple(map(int,x.split())),data_file.read().split("\n")[:-1])

katz(edge_list)


# Implementation of the Katz algorithm
def katz(edge_list):
    train_list, test_list = split_data(edge_list)
    train_graph = Graph(train_list)
    test_graph = Graph(test_list)
    train_n = train_graph.vcount()
    train_vertices_set = get_vertices_set(train_list) # Need this because we have to only consider target users who are present in this train_vertices_set
    test_vertices_set = get_vertices_set(test_list) # Set of target users

    # build a special dict that is like an adjacency list
    katzDict = {}
    adjList = train_graph.get_adjlist()

    for i, l in enumerate(adjList):
        katzDict[i] = l

    sim = [[0 for i in xrange(train_n)] for j in xrange(train_n)]
    for i in xrange(train_n):
        print i
        if i not in train_vertices_set:
            continue

        for j in xrange(i+1, train_n):
            if j in train_vertices_set:     # TODO: check if we need this
                sim[i][j] = sim[j][i] = katz_similarity(katzDict,i,j)

    print_precision_and_recall(sim,train_graph,test_graph,test_vertices_set,train_vertices_set)

# Calculates the Katz Similarity measure for a node pair (i,j)
def katz_similarity(katzDict,i,j):
    l = 1
    neighbors = katzDict[i]
    score = 0

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
    print "Precision is : " + str(precision/c)
    print "Recall is : " + str(recall/c)

