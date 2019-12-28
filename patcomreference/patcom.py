from __future__ import division
import sys
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from collections import Counter
import codecs
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from itertools import combinations
from networkx.algorithms.approximation.steinertree import steiner_tree
import networkx as nx
import matplotlib.pyplot as plt
import operator
import re

stop_words = set(stopwords.words('english') + list(punctuation))
Stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def processing(arg):
    filtered = []
    sentences = str(arg)
    new_string = re.sub(r'[^a-zA-Z]', ' ', sentences)
    new_s = new_string.lower()
    Sentence = sent_tokenize(new_s)
    Words = word_tokenize(new_s)

    for word in Words:
        if word not in stop_words:
            if (len(word) > 3):
                filtered.append(word)

    Nouns = []
    LemmaNoun = []
    tagged_words = nltk.pos_tag(filtered)

    for x in tagged_words:
        if (x[1] == "NN" or x[1] == "NNP" or x[1] == "NNS" or x[1] == "NNPS"):
            Nouns.append(x[0])
    for z in Nouns:
        LemmaNoun.append(lemmatizer.lemmatize(z))

    return (Sentence, Nouns)


def ChiSquareTest(arg1, arg2, arg3):
    FeatureSet = arg1
    countList1 = arg2
    countList2 = arg3
    a = 0
    b = 0

    ChiValueDocA = {}
    ChiValueDocB = {}

    for i in countList1.keys():
        a = a + countList1[i]
    for j in countList2.keys():
        b = b + countList2[j]

    N = a + b  # Total no. of instances (constant)
    P = a  # Number of instances of document1(constant)

    for eachFeature in FeatureSet:
        if (eachFeature in countList1.keys()):

            A = countList1[eachFeature]  # count of occurrence of X in document1
            B = 0

        else:
            B = countList2[eachFeature]  # count of occurrence of X in document1
            A = 0

        M = A + B  # count of occurrence of X in both documents
        chi2 = float((N * (((A * N) - (M * P)) ** 2)) / ((P * M) * (N - P) * (N - M)))

        if (A == 0):

            ChiValueDocB[eachFeature] = chi2

        else:

            ChiValueDocA[eachFeature] = chi2

    return ChiValueDocA, ChiValueDocB


def topFeatures(ChiValueA, ChiValueB):
    ChiSquareValueA = sorted(ChiValueA.items(), key=lambda x: x[1], reverse=True)[:10]

    ChiSquareValueB = sorted(ChiValueB.items(), key=lambda x: x[1], reverse=True)[:10]

    return ChiSquareValueA, ChiSquareValueB


def feature_combination(arg1, arg2):
    Sentence1, result1 = processing(arg1)  # Document A
    countList_1 = Counter(result1)

    Sentence2, result2 = processing(arg2)  # Document B
    countList_2 = Counter(result2)

    OverallFeature = list(set().union(result1, result2))
    CommonFeature = list(set(result2) & set(result1))

    discriFeatSet = []
    for common in OverallFeature:
        if ((common in CommonFeature) == False):
            discriFeatSet.append(common)
    d1 = {}
    for x in countList_1.keys():
        d1[x] = []
        for y in Sentence1:
            if (x in y):
                d1[x].append(Sentence1.index(y))

    d2 = {}
    for x in countList_2.keys():
        d2[x] = []
        for y in Sentence2:
            if (x in y):
                d2[x].append(Sentence2.index(y))

    return d1, d2, countList_1, countList_2, discriFeatSet


def LinkageScore(arg1, arg2):
    sent1, sent2, countList_1, countList_2, DiscrmntvFeat = feature_combination(arg1, arg2)
    val1 = list(combinations(countList_1.keys(), 2))
    val2 = list(combinations(countList_2.keys(), 2))
    G = nx.Graph()

    DictFeat1 = {}
    DictFeat2 = {}

    for x in val1:
        m = list(set(sent1[x[0]]) & set(sent1[x[1]]))
        DictFeat1[x] = len(m)

    for x in val2:
        m = list(set(sent2[x[0]]) & set(sent2[x[1]]))
        DictFeat2[x] = len(m)

    w1 = {}
    w2 = {}
    cnt = 0

    for x in val1:
        n1 = x[0]
        n2 = x[1]
        v = DictFeat1[x]
        v1 = countList_1[n1]
        v2 = countList_1[n2]
        q = v1 * v2
        r = v / q
        value = 2 * r
        w1[x] = value
        cnt = cnt + 1
        '''if(cnt==):
                break
        '''
    cnt = 0
    for x in val2:
        n1 = x[0]
        n2 = x[1]
        v = DictFeat2[x]
        v1 = countList_2[n1]
        v2 = countList_2[n2]
        q = v1 * v2
        r = v / q
        value = 2 * r
        w2[x] = value
        cnt = cnt + 1
        '''if(cnt==100):
                break'''

    new_dict = {}

    for x in w1.keys():
        G.add_edge(*x)
    for y in w2.keys():
        G.add_edge(*y)

    for x in w1.keys():
        if (x in w2.keys()):
            a = (w1[x] + w2[x]) / 2
            if (a > 0.1):
                new_dict[x] = w1[x]
                G.add_edge(*x, weight=a)

    return (new_dict, countList_1, countList_2, DiscrmntvFeat, G)


def Module3(arg1, arg2):
    featPair, cntList1, cntList2, discrmntv, G = LinkageScore(arg1, arg2)
    chiVal_A, chiVal_B = ChiSquareTest(discrmntv, cntList1, cntList2)
    topFeatA, topFeatB = topFeatures(chiVal_A, chiVal_B)

    terminalNodes1 = []
    terminalNodes2 = []

    for x in topFeatA:
        terminalNodes1.append(x[0])

    for y in topFeatB:
        terminalNodes2.append(y[0])

    terminalNodes = terminalNodes1 + terminalNodes2

    sT = steiner_tree(G, terminalNodes)
    return (sT)


def Module4(arg1, arg2):
    sT = Module3(arg1, arg2)
    sTdictionary = {}

    SentenceA = sent_tokenize(str(arg1))
    SentenceB = sent_tokenize(str(arg2))

    for x in SentenceA:
        x = ''.join(x.split())
        x = x.replace("u'", "'", 1)
        x = x.replace('u"', '"', 1)

    for x in SentenceB:
        x = ''.join(x.split())
        x = x.replace("u'", "'", 1)
        x = x.replace('u"', '"', 1)

    Nodes = list(sT.nodes(data=False))

    for eachSentence in SentenceA:
        sTdictionary[eachSentence] = []
        for eachNode in Nodes:
            if (eachNode in eachSentence.lower()):
                sTdictionary[eachSentence].append(eachNode)
    for eachSentence in SentenceB:
        sTdictionary[eachSentence] = []
        for eachNode in Nodes:
            if (eachNode in eachSentence.lower()):
                sTdictionary[eachSentence].append(eachNode)

    SentList = sorted(sTdictionary.items(), key=lambda x: len(x[1]), reverse=True)

    Summary = []
    while (len(Nodes) != 0):
        lst = {}
        for x in SentList:

            l = x[0]
            lst[l] = []
            for i in x[1]:
                if (i in Nodes):
                    lst[l].append(i)

        maxvalue = sorted(lst.items(), key=lambda x: len(x[1]), reverse=True)
        Summarysent = maxvalue[0][0]
        maxLength = maxvalue[0][1]
        SentList = [i for i in SentList if i[0] != Summarysent]
        for j in maxLength:
            Nodes.remove(j)
        Summary.append(Summarysent)
        StringSummary = ""
        for i in Summary:
            StringSummary = StringSummary + str(i)

    return (StringSummary)


if __name__ == '__main__':
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    doc1 = codecs.open(file1, "r", encoding="utf-8")
    doc2 = codecs.open(file2, "r", encoding="utf-8")
    text1 = doc1.readlines()
    text2 = doc2.readlines()
    doc1.close()
    doc2.close()
    summary = Module4(text1, text2)
    print(summary)













