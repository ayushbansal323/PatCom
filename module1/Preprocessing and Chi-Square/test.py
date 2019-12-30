from string import punctuation
from nltk.corpus import stopwords
import Read as rd
import sys
import traceback
import nltk


def getLemmatizedNouns(doc_name):
    document = doc_name
    # get All nouns from document
    nouns = []
    words = []
    from nltk.corpus import words as nltkwords
    nltk_words = nltkwords.words()
    lemmatizer = nltk.WordNetLemmatizer()
    stop_words = set(stopwords.words('english') + list(punctuation))
    for word in document.split():
        # function to test if something is a noun
        #print(word)
        #print(word)
        if len(word) > 2 and word not in stop_words:
            words.append(word.lower())
    # tagged_words are words tagged as nouns, Adjective etc.
    tagged_words = nltk.pos_tag(words)
    for x in tagged_words:
        if x[1] == "NN" or x[1] == "NNP" or x[1] == "NNS" or x[1] == "NNPS":
            # condition to check if the word is an english word.
            if x[0] in nltk_words:
                nouns.append(lemmatizer.lemmatize(x[0]))
    # print(nouns)
    return nouns

str="A jet regulator of jet regulator having an interior in which a jet device is provided that has openings that extend across of the Said openings being offset with respect to one another in a direction about the jet regulator or in a direction of flow of the jet regulator where in the jet device has at least one insertable containing the openings and wherein the at least one insertable a number of insertable that can be inserted one after another in the direction of flow into the jet regulator the insertable have a peripheral external support ring and that are connected to the Support ring on an inside thereof and that extend from one end to another across a flow of the and the of the insertable  are parallel So that the openings are unidirectionally oriented."
n = getLemmatizedNouns(str)
s=set(n)
print("&"*50)
print(s)

print(n)
