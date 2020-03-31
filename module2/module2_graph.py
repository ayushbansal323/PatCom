import PyPDF2
import regex
import networkx as nx
import matplotlib.pyplot as plt
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from module1.chisquare.Read import read_document

def connected_component_subgraphs(G):
    for c in nx.connected_components(G):
        yield G.subgraph(c)

def find_scores(features, document_lines):
    """
    :param features: list of feature
    :param document_path: path where the document is located
    :return: list containing occurrence of each feature in the document
    """
    features_count = {}

    for feature in features:
        features_count[feature] = 0

    for feature in features:
        for line in document_lines:
            count = line.count(feature)
            if count:
                features_count[feature] = features_count[feature] + count
    return features_count


def features_union(feature_1, feature_2):
    """
    :param feature_1: list containing features of document 1
    :param feature_2: list containing features of document 2
    :return: list containing features of document 1 and document 2
    """
    features = feature_1 + feature_2
    unique_features = []
    for i in range(len(features)):
        flag = 1
        for j in range(i + 1, len(features)):
            if features[i] == features[j]:
                flag = 0
        if flag:
            unique_features.append(features[i])
    return unique_features


def linkage_score(vertex1, vertex2, document_lines, count1, count2):
    """
    :param vertex1: feature 1
    :param vertex2: feature 2
    :param document_lines: list containing lines of document
    :param count1: occurrence of feature 1 in the document
    :param count2: occurrence of feature 2 in the document
    :return: linkage score between vertex1 and vertex2
    """
    count12 = 0
    for line in document_lines:
        if (vertex1 in line) and (vertex2 in line):
            count12 = count12 + 1
    score = 0
    if count12 != 0:
        score = (2 * count12) / (count1 + count2)
    return score


def generate_graph(features1, features2, document_lines1, document_lines2, threshold_value):
    """
    :param threshold_value: the minimum linkage score needed to connect the edges
    :param features1: list containing feature for document 1
    :param features2: list containing feature for document 2
    :param document_path1: path to the document file 1
    :param document_path2: path to the document file 2
    :return: graph
    """
    features = features_union(features1, features2)
    features.sort()
    score1 = find_scores(features, document_lines1)
    score2 = find_scores(features, document_lines2)
    # print(score1)
    # print(score2)
    graph = nx.Graph()
    lemmatizer = WordNetLemmatizer()

    for i in range(len(features)):
        graph.add_node(features[i])

    for i in range(len(features)):
        for j in range(i + 1, len(features)):
            link_score1 = linkage_score(features[i], features[j], document_lines1, score1[features[i]],
                                        score1[features[j]])
            link_score2 = linkage_score(features[i], features[j], document_lines2, score2[features[i]],
                                        score2[features[j]])
            link_score = (link_score1 + link_score2) / 2
            if link_score > threshold_value:
                temp1=wn.synsets(lemmatizer.lemmatize(features[i]))
                temp2=wn.synsets(lemmatizer.lemmatize(features[j]))
                if len(temp2) == 0 or len(temp1) == 0:
                    #print(features[i]+"\t"+features[j])
                    if len(temp2) == 0 and len(temp1) == 0:
                        graph.add_edge(features[i], features[j], weight=link_score)
                    else:
                        graph.add_edge(features[i], features[j], weight=(link_score+0.001))
                else:
                    wup_score = temp1[0].wup_similarity(temp2[0])
                    #print(wup_score)
                    if wup_score == None:
                        graph.add_edge(features[i], features[j], weight=(link_score+0.002))
                    else:
                        graph.add_edge(features[i], features[j], weight=(link_score+(wup_score/10)))
                #print(features[i]+ features[j])
                #print(graph.get_edge_data(features[i], features[j]))
            # print(link_score)
     
    
    graph = max(connected_component_subgraphs(graph), key=len)
    #nx.draw_networkx(graph, nx.spring_layout(graph))
    #plt.show()
    
    # print(graph.number_of_nodes())
    # print(graph.number_of_edges())

    return graph


if __name__ == '__main__':
    feature1 = ["regulator", "housing", "device", "anti-Scaling", "passage", "openings", "network"]
    feature2 = ["regulator", "housing", "device", "anti-Scaling", "passage", "openings", "network"]
    doc1 = read_document("./Document_1.pdf")
    doc2 = read_document("./Document_2.pdf")
    generate_graph(feature1, feature2, doc1, doc2, 0.1)
