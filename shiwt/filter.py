import sys


def main(argv=None):
    if argv is None:
        argv = sys.argv

    train_set = set()
    with open(argv[2], 'r') as f:
        for line in f:
            [a, b] = line.split()
            train_set.add((a, b))

    with open(argv[3], 'w+') as out_file:
        with open(argv[1], 'r') as in_file:
            for line in in_file:
                [a, b, rate] = line.split()
                if (a, b) not in train_set and (b, a) not in train_set:
                    out_file.write(line)


if __name__ == "__main__":
    main()
