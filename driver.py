import networkx as nx
from module1.chisquare.Extract_Features import module1
from module1.chisquare.Read import read_document
from module1.Semantic_Analayser import Wordnet_submodule
from module2 import module2_graph
from module3 import tree_extraction
from module4 import module_4
import matplotlib.pyplot as plt
import os

def driver_code( doc1_path , doc2_path ):
    # Module 1 Part 1
    # Read and Chi-Square
    doc1 = read_document( doc1_path )
    doc2 = read_document( doc2_path )
    # if needed change threshold in Extract_Features.py
    doc1_feature_dic, doc2_feature_dic, nouns_doc1, nouns_doc2 = module1(doc1, doc2)
    print("*"*50)

    # Module 1 Part 2
    # Wordnet
    # passing all nouns present in both the documents.
    feature_dic1 = list(doc1_feature_dic.keys())
    feature_dic2 = list(doc2_feature_dic.keys())
    feature_dic1.sort()
    feature_dic2.sort()
    gen_and_comp_features, gen_features = Wordnet_submodule.wordnetModule(feature_dic1+feature_dic2)


    #module 2 called
    graph = module2_graph.generate_graph(nouns_doc1, nouns_doc2, doc1, doc2, 0.13)

    #module 3
    gen_and_comp_features.sort()
    edges = sorted(graph.edges(data=True), key=lambda t: t[2].get('weight', 1))
    tree = tree_extraction.module3(graph, gen_and_comp_features)

    #module 4
    ans = module_4.Create_Summary(nx.Graph(tree),gen_features,doc1,doc2)
    return ans
