import PyPDF2
import regex
import networkx as nx
import matplotlib.pyplot as plt
# function defined in read.py
def read_document(path):
    """
    :param path: path of the document
    :return: returns a list of lines in document
    """
    Document_1 = []

    fd = open(path, 'rb');

    file_reader = PyPDF2.PdfFileReader(fd);

    for i in range(0, file_reader.numPages):
        page = file_reader.getPage(i);
        Document_1.append(page.extractText());

    index = Document_1[0].find('ABSTRACT');

    Document_1[0] = Document_1[0][index:]

    output = []

    for i in range(0, file_reader.numPages):
        Document_1[i] = regex.sub('(\(.*?\))|(\S*?[+*/%]+\S*)|([0-9]+[Ee.]+[0-9]+)|([0-9]+\S*)|(FIG.)', '',
                                  Document_1[i]);
        output += Document_1[i].split('.')

    return output;


def find_scores(features, document_path):
    """
    :param features: list of feature
    :param document_path: path where the document is located
    :return: list containing occurrence of each feature in the document
    """
    document_lines = read_document(document_path)
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


def module2(features1, features2, document_path1, document_path2):
    """
    :param features1: list containing feature for document 1
    :param features2: list containing feature for document 2
    :param document_path1: path to the document file 1
    :param document_path2: path to the document file 2
    :return: graph
    """
    features = features_union(features1, features2)
    document_lines1 = read_document(document_path1)
    document_lines2 = read_document(document_path2)
    score1 = find_scores(features, document_path1)
    score2 = find_scores(features, document_path2)
    # print(score1)
    # print(score2)
    count = 0
    graph = nx.Graph()
    for i in range(len(features)):
        for j in range(i + 1, len(features)):
            link_score1 = linkage_score(features[i], features[j], document_lines1, score1[features[i]], score1[features[j]])
            link_score2 = linkage_score(features[i], features[j], document_lines2, score2[features[i]], score2[features[j]])
            link_score = (link_score1 + link_score2) / 2
            if link_score > 0.1:
                graph.add_edge(features[i], features[j])
            #print(link_score)
    nx.draw_networkx(graph, nx.spring_layout(graph))
    #nx.draw_circular(graph)
    plt.show()
    #print(graph.number_of_nodes())
    #print(graph.number_of_edges())

    return graph


if __name__ == '__main__':
    feature1 = ["regulator", "housing", "device", "anti-Scaling", "passage", "openings", "network"]
    feature2 = ["regulator", "housing", "device", "anti-Scaling", "passage", "openings", "network"]
    document1 = "./Document_1.pdf"
    document2 = "./Document_2.pdf"
    module2(feature1, feature2, document1, document2)
