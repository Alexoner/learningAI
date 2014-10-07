# Hierarchical clustering

# load file


def readfile(filename):
    lines = [line for line in file(filename)]

    # First line is the column titles
    colnames = lines[0].strip().split('\t')[1:]
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # First column in each row is the rowname
        rownames.append(p[0])
        # The data for this row is the ramainder of the row
        data.append([float(x) for x in p[1:]])

    return rownames, colnames, data

# define closeness
# Pearson correlation coefficient
from math import sqrt


# The final line is to create a smaller distance between items that are
# more similar
def pearson(v1, v2):
    # Simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    # Sums of the squares
    sum1sq = sum([pow(v, 2) for v in v1])
    sum2sq = sum([pow(v, 2) for v in v2])

    # Sum of the products
    pSum = sum([v1[i] * v2[i] for i in xrange(len(v1))])

    # Calculate r (Pearson score)
    num = pSum - (sum1 * sum2) / len(v1)
    den = sqrt((sum1sq - pow(sum1, 2) / len(v1))
               * (sum2sq - pow(sum2, 2) / len(v1)))
    if den == 0:
        return 0

    return 1.0 - num / den

# Each cluster in a hierarchical clustering algorithm is either a point in
# the tree with two branches, or an endpoint associated with an actual row
# from the dataset (in this case, a blog).
# Each cluster also contains data about its location,which is either the
# row data for the endpoints or the merged data from its two branches for
# other node types.


class bicluster:

    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance
