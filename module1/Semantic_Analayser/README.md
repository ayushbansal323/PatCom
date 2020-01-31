Wordnet Module:
It uses wordnet library from nltk.corpus.
There are 3 functions in this module as:

1. wordSimilarity():
    -It takes input as word of which the symantics is to be compared(2nd input i.e. wodList)
    -There are multiplee synsets in wordnet so we consider every synset which is noun and add it to list named similarity with its initial score as 0.
    -It is guaranteed that minimum one synset exists as words with zero synsets are expected to be filtered in previous module.
    -For every synset present we calculate its similarity with every other word in wordList.
    -Output is [word, most approiate synset, how many words in wordList are similar to word]
    
2. countChild():
    -It takes input as synset (say syn) whose children are to be detected and list from which it is calculated.
    -It returns number of child present.
    -For every word in input list we do:
        -Check if in hierarcy the parent(syn) is above child, if not do not consider it.
        -If present then we calculate average similarity between parent(syn) and child's hypernyms(these are parents according to wordNet DB)
        -If that average is above some threshold then we just increment children count
        
3. wordnetModule():
    -Here similar words are grouped together and also general features are also extracted.
    -Remove elements which are not present as nouns in wordnetDB.
    -check similarity for each element and if above threshold then only consider them, hence removing Outliers.
    -Check for each word how many children it has and if above threshold then consider that word as general feature.
    -Return features without outliers and also general features.

4. calculate_score():
    -Score of each word in list1 is calculated with every word in list2 and same for words in list2.
    -Remove elements which are not present as nouns in wordnetDB.
    -check similarity for each element with other lists every element and store count of similar words in dictionary
    -It outputs 2 dictionary which contains words and count of similar words present in other list.