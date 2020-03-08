from networkx.algorithms.approximation.steinertree import steiner_tree

#Input      : (@networkx.graph : G) graph of two patents combined
#           : (@list of string : topFeatuers) discrimitive features of two documents
#Output     : (@networkx.steiner_tree) Steiner tree
def module3(G, topFeatures):
    sT = steiner_tree(G, topFeatures, weight='weight')
    return sT