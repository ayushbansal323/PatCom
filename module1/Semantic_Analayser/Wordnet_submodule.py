try:
    from nltk.corpus import wordnet as wn
except LookupError:
    import nltk
    nltk.download('wordnet')
    from nltk.corpus import wordnet as wn


# Input      : (@string : word) word whose similarity with all other words in document is to be calculated
#             (@list of string : wordlist) list of words in document
# Output     : (@string : ret[0]) '@word'
#             (@synset : ret[1]) most approtiate synset describing the word
#             (@integer : ret[2]) number of words in wordlist who have similarity above threshold
def wordSimilarity(word, wordList):
    wordsyn = wn.synsets(word, 'n')
    similarity = [0] * len(wordsyn)  # to determine similarity with all synsets
    threshold = 0.5  # minimum similarity index required

    for i in range(len(wordsyn)):
        for jword in wordList:
            if jword != word:
                temp = 0
                for jwordsyn in wn.synsets(jword, 'n'):
                    temp += wordsyn[i].wup_similarity(jwordsyn)
                temp = temp / (len(wn.synsets(jword, 'n')))  # average similarity with all synsets of jword
                if temp >= threshold:
                    similarity[i] += 1

    i = similarity.index(max(similarity))  # identify which synset has max similarity
    return [word, wordsyn[i], similarity[i]]


# Input      : (@synset : syn) most relevant synonym w.r.t. wordnet DB
#             (@list : filtered) each element in list contains word, synset, similar words
# Output     : (@integer : child) Number of child a word has which are present in '@filtered'
def countChild(syn, filtered):
    threshold = 0.5  # minimum similarity index required
    child = 0

    for _, feature, _ in filtered:
        if syn.max_depth() < feature.max_depth() - 1:
            temp = 0
            for wordsyn in feature.hypernyms():
                temp += syn.wup_similarity(wordsyn)
            if temp / len(feature.hypernyms()) >= threshold:
                child += 1
    return child


# Input      : (@list of string : wordList) list of words
# Output     : (@list of string: ret[0]) containing general features + comparitive features
#             (@list of string: ret[1]) general features
def wordnetModule(wordList):
    threshold = 0.2  # if 20 percent of words are similar to a word then it is considered
    filtered = []  # list without outliers
    # determine outliers, by calculating how many words are similar to given word
    for word in wordList:
        temp = wordSimilarity(word, wordList)
        if temp[2] / len(wordList) >= threshold:
            filtered.append(temp)

    # determine general or common features
    generalFeature = []
    general_feature_threshold = 0.2  # if 20 percent features in document are children of any feature then it is general feature
    # check how many childrens does a word have
    for temp in filtered:
        child = countChild(temp[1], filtered)
        if child / len(wordList) >= general_feature_threshold:
            generalFeature.append([temp[0], child])

    return [x[0] for x in filtered], [x[0] for x in generalFeature]


def test():
    wordList = ['dog', 'cat', 'domestic', 'goa', 'mammal', 'car', 'animal', 'pet']
    print(wordnetModule(wordList))


