import networkx as nx
from module1.chisquare.Extract_Features import module1
from module1.chisquare.Read import read_document
from module1.Semantic_Analayser import Wordnet_submodule
from module2 import module2_graph
from module3 import tree_extraction
from module4 import module_4
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Module 1 Part 1
    # Read and Chi-Square

    import os
    doc1 = read_document("./Document_1.pdf")
    doc2 = read_document("./Document_2.pdf")
    #print(doc1 , doc2)
    # if needed change threshold in Extract_Features.py
    doc1_feature_dic, doc2_feature_dic, nouns_doc1, nouns_doc2 = module1(doc1, doc2)
    #print(nouns_doc2)

    #print(doc1_feature_dic)
    print("*"*50)
    #print(doc2_feature_dic)

    # Module 1 Part 2
    # Wordnet

    # passing all nouns present in both the documents.
    #print(list(doc1_feature_dic.keys())+list(doc2_feature_dic.keys()))
    # this gives div by 0 error.
    feature_dic1 = list(doc1_feature_dic.keys())
    feature_dic2 = list(doc2_feature_dic.keys())
    feature_dic1.sort()
    feature_dic2.sort()
    gen_and_comp_features, gen_features = Wordnet_submodule.wordnetModule(feature_dic1+feature_dic2)


    #module 2 called
    graph = module2_graph.generate_graph(nouns_doc1, nouns_doc2, "./Document_1.pdf", "./Document_2.pdf", 0.1)
    ###########################################
    #module 3
    #topfeatures = module2_graph.features_union(list(doc1_feature_dic.keys()), list(doc2_feature_dic.keys()))
    #module 3
    tree = tree_extraction.module3(graph, gen_and_comp_features)

    nx.draw_networkx(tree, nx.spring_layout(tree))
    #nx.draw_circular(graph)
    plt.show()
    #module 4
    ans = module_4.Create_Summary(nx.Graph(tree),gen_features,doc1,doc2)
    print(ans)

    # Module 1 Part 2
    # Wordnet - this will return 2 list. Give the 1st list to 3rd module and 2nd list to 4th module.



