from module1.chisquare.Extract_Features import module1
from module1.chisquare.Read import read_document
from module2 import module2_graph

if __name__ == "__main__":
    # Module 1 Part 1
    # Read and Chi-Square

    import os
    doc1 = read_document("./Document_1.pdf")
    doc2 = read_document("./Document_2.pdf")
    # if needed change threshold in Extract_Features.py
    doc1_feature_dic, doc2_feature_dic = module1(doc1, doc2)

    print(doc1_feature_dic)
    print("*"*50)
    print(doc2_feature_dic)

    #module2 calling function replace dic_features with actual features
    module2_graph.generate_graph(list(doc1_feature_dic.keys()), list(doc2_feature_dic.keys()), "./Document_1.pdf", "./Document_2.pdf", 0.1)
    ###########################################

    # Module 1 Part 2
    # Wordnet - this will return 2 list. Give the 1st list to 3rd module and 2nd list to 4th module.



