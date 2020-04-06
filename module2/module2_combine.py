import PyPDF2
import regex
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.approximation.steinertree import steiner_tree
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer


def combine_nodes(graph):
    lemmatizer = WordNetLemmatizer()
    for feature1 in graph.nodes():
        for feature2 in graph.nodes():
            if feature1 != feature2:
                temp1 = wn.synsets(lemmatizer.lemmatize(feature1))
                temp2 = wn.synsets(lemmatizer.lemmatize(feature2))
                if len(temp2) != 0 and len(temp1) != 0:
                    path_score = temp1[0].path_similarity(temp2[0])
                    # print(wup_score)
                    if path_score != None and path_score > 0.5 :
                        graph = nx.contracted_nodes(graph, feature1 , feature2)
                        print(feature1+feature2+"@!4")
    return graph
