import networkx as nx


def similarity_score(tree, doc1, doc2):
    edges = list(tree.edges)
    common_edges = 0
    uncommom_edges = 0
    com_edge = []
    for edge in edges:
        present_in_doc1 = False
        present_in_doc2 = False
        for line in doc1:
            if(edge[0] in line) and (edge[1] in line):
                present_in_doc1 = True
                break
        for line in doc2:
            if (edge[0] in line) and (edge[1] in line):
                present_in_doc2 = True
                break
        if present_in_doc1 and present_in_doc2:
            common_edges = common_edges + 1
            com_edge.append(edge)
        elif present_in_doc1 or present_in_doc2:
            uncommom_edges = uncommom_edges + 1

    score = (100 * common_edges) / len(edges)
    return score
