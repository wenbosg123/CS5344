import re
import sys
from pyspark import SparkConf, SparkContext
import math


def line_to_feature(line):
    arr = re.split(r'[^\w]+', line)
    features = []
    user_id = arr[0]
    for feat_id in range(1, len(arr)):
        val = int(arr[feat_id])
        if val > 0:
            features.append((user_id, (feat_id, val)))
    return features


def main(argv=None):
    if argv is None:
        argv = sys.argv

    conf = SparkConf()
    sc = SparkContext(conf=conf)

    lines = sc.textFile(sys.argv[1])
    features = lines.flatMap(line_to_feature)
    s = features.map(lambda t: (t[0], t[1][1] ** 2)).reduceByKey(lambda a, b: a + b).map(
        lambda t: (t[0], math.sqrt(t[1])))
    normalized_features = features.join(s).map(lambda t: (t[1][0][0], (t[0], t[1][0][1] / t[1][1])))
    relevance = normalized_features.join(normalized_features).filter(lambda t: int(t[1][0][0]) < int(t[1][1][0])).map(
        lambda t: ((t[1][0][0], t[1][1][0]), t[1][0][1] * t[1][1][1])).reduceByKey(lambda a, b: a + b)
    result = relevance.sortBy(lambda t: t[1], ascending=False).collect()

    with open(sys.argv[2], 'w+') as f:
        for r in result:
            f.write('%s %s %f\n' % (r[0][0], r[0][1], r[1]))

    sc.stop()


if __name__ == "__main__":
    main()
