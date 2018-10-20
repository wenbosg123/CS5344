import sys
import random

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()
partitions = int(sys.argv[2])
chunks = [[] for i in range(partitions)]
for line in lines:
    chunks[random.randrange(0, partitions)].append(line)

for i in range(partitions):
    with open("test_set_" + str(i) + ".txt", 'w+') as f:
        for line in chunks[i]:
            f.write("%s\n" % line)
    with open("train_set_" + str(i) + ".txt", 'w+') as f:
        for j in range(partitions):
            if i == j:
                continue
            for line in chunks[j]:
                f.write("%s\n" % line)
