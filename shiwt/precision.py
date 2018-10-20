import sys

edges = set()
with open(sys.argv[2]) as f:
    for line in f:
        arr = line.split()
        edges.add((arr[0], arr[1]))

prediction_size = int(sys.argv[3])
hit_num = 0
with open(sys.argv[1]) as f:
    for i in range(prediction_size):
        arr = f.readline().split()
        if (arr[0], arr[1]) in edges or (arr[1], arr[0]) in edges:
            hit_num += 1
print('Hit %d out of %d\nPrecision: %f' % (hit_num, prediction_size, hit_num / prediction_size))
