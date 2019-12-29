try:
    from nltk.corpus import wordnet as wn
except LookupError:
    import nltk
    nltk.download('wordnet')
    from nltk.corpus import wordnet as wn


def wordSimilarity(word,wordList):
    wordsyn = wn.synsets(word, 'n')
    similarity = [0] * len(wordsyn)
    threshold = 0.5#minimum similarity index required

    for i in range(len(wordsyn)):
        for jword in wordList:
            if jword != word:
                temp = 0
                for jwordsyn in wn.synsets(jword, 'n'):
                    temp += wordsyn[i].wup_similarity(jwordsyn)
                temp = temp/(len(wn.synsets(jword, 'n')))
                if temp >= threshold:
                    similarity[i] += 1

    i = similarity.index(max(similarity))
    return [word,wordsyn[i],similarity[i]]

def countChild(syn, filtered):
    threshold = 0.5#minimum similarity index required
    child = 0

    for _,feature,_ in filtered:
        if syn.max_depth() < feature.max_depth()-1:
            temp = 0
            for wordsyn in feature.hypernyms():
                temp += syn.wup_similarity(wordsyn)
            if temp/len(feature.hypernyms()) >= threshold:
                child += 1
    return child


def wordnetModule(wordList):
    threshold = 0.2 #if 20 percent of words are similar to a word then it is considered
    filtered = []
    for word in wordList:
        temp = wordSimilarity(word,wordList)
        if temp[2]/len(wordList) >= threshold:
            filtered.append(temp)

    generalFeature = []
    general_feature_threshold = 0.2#if 20 percent features in document are children of any feature then it is general feature
    for temp in filtered:
        child = countChild(temp[1],filtered)
        if child/len(wordList) >= general_feature_threshold:
            generalFeature.append([temp[0],child])

    return [x[0] for x in filtered],generalFeature

def test():
    wordList = ['dog', 'cat', 'domestic', 'goa', 'mammal','car','animal','pet']
    print(wordnetModule(wordList))

test()