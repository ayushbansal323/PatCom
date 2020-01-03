from string import punctuation
from nltk.corpus import stopwords
import sys
import traceback
import nltk

# decrese this threshold to increses the number of features
CHI_THRESHOLD = 0.01

# returns lemmatized nouns in lower case
def getLemmatizedNouns(document):
    #document = rd.read_document(doc_path)
    # get All nouns from document
    nouns = []
    words = []
    from nltk.corpus import words as nltkwords
    nltk_words = nltkwords.words()
    lemmatizer = nltk.WordNetLemmatizer()
    stop_words = set(stopwords.words('english') + list(punctuation))
    for lines in document:
        # function to test if something is a noun
        words_array = lines.split()
        for word in words_array:
            if len(word) > 2 and word not in stop_words:
                words.append(word.lower())
    # tagged_words are words tagged as nouns, Adjective etc.
    tagged_words = nltk.pos_tag(words)
    for x in tagged_words:
        # check if the word is noun
        if x[1] == "NN" or x[1] == "NNP" or x[1] == "NNS" or x[1] == "NNPS":
            # condition to check if the word is an english word.
            if x[0] in nltk_words:
                nouns.append(lemmatizer.lemmatize(x[0]))
    # print(nouns)
    return nouns


# create a dictionary of nouns with their count in doc A and doc B
def create_dict(nounsdoc1, nounsdoc2):
    nouns_dict = {}
    sum_count_doc1 = 0
    sum_count_doc2 = 0
    for n in set().union(nounsdoc1, nounsdoc2):
        if n not in nouns_dict:
            count_in_doc1 = nounsdoc1.count(n)                  # count of noun in document
            count_in_doc2 = nounsdoc2.count(n)
            nouns_dict[n] = [count_in_doc1, count_in_doc2]
            sum_count_doc1 += count_in_doc1                     # sum of all words.
            sum_count_doc2 += count_in_doc2
    return nouns_dict, sum_count_doc1, sum_count_doc2


# edit this later
def main():
    print("---Features Extraction ---")
    print("Application name: {}".format(sys.argv[0]))

    if len(sys.argv) < 3 or len(sys.argv) > 3:
        print("ERR: Invalid Number of Args")

    if sys.argv[1].lower == "-h":
        print("This is a part of Patcom which extracts Nouns and qulifies them with chi square.")
        exit()

    if sys.argv[1].lower == "-u":
        print("Usage: Appname Target_Doc1 Target_Doc2")
        exit()

    if len(sys.argv) != 4:
        print("ERR: Invalid no of Args")
        exit()

    try:
        pass

    except Exception as e:
        print("ERR: Invalid Input" + str(e))
        print(traceback.format_exc())


def chisquare(noun_dict, sum_doc1, sum_doc2):
    chisq_dict = {}
    for x in noun_dict:
        a = noun_dict[x][0]  # A is the number of times t and c co-occur
        b = noun_dict[x][1]  # B is the number of times t occurs without c
        c = sum_doc1 - a
        d = sum_doc2 - b
        # c=1
        # d=1
        chi = ((2 * ((a * d) - (c * b)) ** 2) / ((a + c) * (b + d) * (a + b) * (c + d)))

        if chi > CHI_THRESHOLD:
            #print(x + " : " + str(chi))
            # print(x)
            chisq_dict[x] = chi
    return chisq_dict


def module1(doc1, doc2):
    # main()
    nouns_doc1 = getLemmatizedNouns(doc1)
    nouns_doc2 = getLemmatizedNouns(doc2)
    # print(nouns_doc1)
    # print(nouns_doc2)
    #
    # print(len(nouns_doc1))
    # print(len(nouns_doc2))

    noun_dict, sum_doc1, sum_doc2 = create_dict(nouns_doc1, nouns_doc2)

    # dict with chi sq values
    print("Calculating chi-square values for features/nouns... It may take some time...")
    chi_sq_doc1 = chisquare(noun_dict, sum_doc1, sum_doc2)
    #print('*'*50)
    chi_sq_doc2 = chisquare(noun_dict, sum_doc2, sum_doc1)
    print("^"*50)

    return chi_sq_doc1,chi_sq_doc2,nouns_doc1,nouns_doc2

