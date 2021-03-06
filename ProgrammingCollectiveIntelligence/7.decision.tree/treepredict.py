"""
    Decision tree learning.

"""

# predicting signups
my_data = [['slashdot', 'USA', 'yes', 18, 'None'],
           ['google', 'France', 'yes', 23, 'Premium'],
           ['digg', 'USA', 'yes', 24, 'Basic'],
           ['kiwitobes', 'France', 'yes', 23, 'Basic'],
           ['google', 'UK', 'no', 21, 'Premium'],
           ['(direct)', 'New Zealand', 'no', 12, 'None'],
           ['(direct)', 'UK', 'no', 21, 'Basic'],
           ['googel', 'USA', 'no', 24, 'Premium'],
           ['slashdot', 'France', 'yes', 19, 'None'],
           ['digg', 'USA', 'no', 18, 'None'],
           ['google', 'UK', 'no', 18, 'None'],
           ['kiwitobes', 'UK', 'no', 19, 'None'],
           ['digg', 'New Zealand', 'yes', 12, 'Basic'],
           ['slashdot', 'UK', 'no', 21, 'None'],
           ['google', 'UK', 'yes', 18, 'Basic'],
           ['kiwitobes', 'France', 'yes', 19, 'Basic']]


# represent a decision tree
class decisionnode:

    def __init__(self, col=-1, value=None, results=None, tb=None, fb=None):
        '''
        @col:the column index of the criteria to be tested
        @value:the value that the column must match to get a true result
        @tb,@fb:decisionnodes,which are the next nodes in the tree if the
            result is true or false,respectively.
        @results:a dictionary of results for this branch.None for everything
            except endpoints.
        '''
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb

# training the tree,using an algorithm called CART(Classification and
# Regression Trees).
# Divides a set on a specific column.Can handle numeric or nominal values


def divideset(rows, column, value):
    # Make a function that tells us if a row is in
    # the first group (true) or the second group (false)
    split_function = None
    if isinstance(value, int) or isinstance(value, float):
        split_function = lambda row: row[column] >= value
    else:
        split_function = lambda row: row[column] == value

    # divide the rows into two sets and return them
    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    return (set1, set2)


def uniquecounts(rows):
# create counts of possible results (the last column of each row is the
# result)
    results = {}
    for row in rows:
    # The result is the last column
        r = row[len(row) - 1]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results

# Two different metrics for measuring how mixed a set is:
# Gini impurity and entroy
# Gini impurity is the expected error rate if one of the results from a set
# is randomly applied to one of the items in the set.
# Probability that a randomly placed item will be in the wrong category


def giniimpurity(rows):
    total = len(rows)
    counts = uniquecounts(rows)
    imp = 0
    for k1 in counts:
        p1 = float(counts[k1]) / total
        for k2 in counts:
            if k1 == k2:
                continue
            p2 = float(counts[k2]) / total
            imp += p1 * p2
    return imp

# Entropy,in information theory,is the amount of disorder in a set
# Basically,how mixed a set is.
# Entropy is the sumof p(x)log(p(x)) across all the different possible
# results


def entropy(rows):
    """
    p(i) = frequence(outcome)=count(outcome)/count(total rows)
    Entropy = sum of p(i) x log(p(i)) for all outcomes
    """
    from math import log
    log2 = lambda x: log(x) / log(2)
    results = uniquecounts(rows)
    # Now calculate the entropy
    ent = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        ent = ent - p * log2(p)
    return ent

# recursive tree building


def buildtree(rows, scoref=entropy):
    """
    To see how good an attribute is,the algorithm first calculates the
    entropy of the whole group.Then it tries DIVIDING up the group by the
    possible values of each ATTRIBUTE and calculate the ENTROPY of the two
    new groups.To determine which attribute is the best to divide on,the
    INFORMATION GAIN is calculated.
    Information gain is the difference between the current entropy and the
    weighted-average entropy of the two new groups.
    The algorithm calculate the information gain for every attribute and
    chooses the one with the highest information gain.
    After the condition for the root node has been decided,the algorithm
    creates two branches corresponding to true or false for that condition.
    """
    if len(rows) == 0:
        return decisionnode()
    current_score = scoref(rows)

    # set up some variables to track the best criteria
    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1
    for col in range(0, column_count):
        # Generate the list of different values in this column
        column_values = {}
        for row in rows:
            column_values[row[col]] = 1
        # Now try dividing the rows up for each value in this column
        for value in column_values.keys():
            (set1, set2) = divideset(rows, col, value)

            # Information gain
            p = float(len(set1)) / len(rows)
            gain = current_score - p * scoref(set1) - (1 - p) * scoref(set2)
            if gain > best_gain and len(set1) > 0 and len(set2) > 0:
                best_gain = gain
                best_criteria = (col, value)
                best_sets = (set1, set2)

    # Create the subbranches
    if best_gain > 0:
        trueBranch = buildtree(best_sets[0])
        falseBranch = buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0], value=best_criteria[1],
                            tb=trueBranch, fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))

# Displaying the tree


def printtree(tree, indent=''):
    # Is this a leaf node?
    if tree.results != None:
        print str(tree.results)
    else:
        # Print the criteria
        print str(tree.col) + ':' + str(tree.value) + '?'

        # print the branches
        print indent + 'T->',
        printtree(tree.tb, indent + '  ')
        print indent + 'F->',
        printtree(tree.fb, indent + '  ')

# graphical display


def getwidth(tree):
    if tree.tb == None and tree.fb == None:
        return 1
    return getwidth(tree.tb) + getwidth(tree.fb)


def getdepth(tree):
    if tree.tb == None and tree.fb == None:
        return 0
    return max(getdepth(tree.tb), getdepth(tree.fb)) + 1


def drawtree(tree, jpeg='tree.jpg'):
    from PIL import Image, ImageDraw
    w = getwidth(tree) * 100
    h = getdepth(tree) * 100 + 120

    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    drawnode(draw, tree, w / 2, 20)
    img.save(jpeg, 'JPEG')


def drawnode(draw, tree, x, y):
    if tree.results == None:
        # Get the width of each branch
        w1 = getwidth(tree.fb) * 100
        w2 = getwidth(tree.tb) * 100

        # Determine the total space required by this node
        left = x - (w1 + w2) / 2
        right = x + (w1 + w2) / 2

        # Draw the condition string
        draw.text((x - 20, y - 10), str(tree.col)
                  + ':' + str(tree.value), (0, 0, 0))

        # Draw links to the branches
        draw.line((x, y, left + w1 / 2, y + 100), fill=(255, 0, 0))
        draw.line((x, y, right - w2 / 2, y + 100), fill=(255, 0, 0))

        # Draw the branch nodes
        drawnode(draw, tree.fb, left + w1 / 2, y + 100)
        drawnode(draw, tree.tb, right - w2 / 2, y + 100)
    else:
        txt = ' \n'.join(['%s:%d' % v for v in tree.results.items()])
        draw.text((x - 20, y), txt, (0, 0, 0))

if __name__ == "__main__":
    # my_data = [line.split('\t')
               # for line in file('desicion_tree_example.txt')]
    print "giniimpurity of my_data: ", giniimpurity(my_data)
    print "entropy of my_data: ", entropy(my_data)
    set1, set2 = divideset(my_data, 2, 'yes')
    print "giniimpurity of set1: ", giniimpurity(set1)
    print "entropy of set1: ", entropy(set1)
    tree = buildtree(my_data)
    printtree(tree)
    drawtree(tree, jpeg='treeview.jpg')
