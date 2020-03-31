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
    threshold = 0.3  # minimum similarity index required

    for i in range(len(wordsyn)):
        for jword in wordList:
            if jword != word:
                temp = 0
                for jwordsyn in wn.synsets(jword, 'n'):
                    temp += wordsyn[i].wup_similarity(jwordsyn)
                if len(wn.synsets(jword, 'n')) != 0:
                    temp = temp / (len(wn.synsets(jword, 'n')))  # average similarity with all synsets of jword
                    if temp >= threshold:
                         similarity[i] += 1

    i = similarity.index(max(similarity))  # identify which synset has max similarity
    return [word, wordsyn[i], similarity[i]]


# Input      : (@synset : syn) most relevant synonym w.r.t. wordnet DB
#             (@list : filtered) each element in list contains word, synset, similar words
# Output     : (@integer : child) Number of child a word has which are present in '@filtered'
def countChild(syn, filtered):
    threshold = 0.3  # minimum similarity index required
    child = 0

    for _, feature, _ in filtered:
        if syn.max_depth() < feature.max_depth() - 1:
            temp = 0
            for wordsyn in feature.hypernyms():
                temp += syn.wup_similarity(wordsyn)
            if len(feature.hypernyms()) != 0 and temp / len(feature.hypernyms()) >= threshold:
                child += 1
    return child


# Input      : (@list of string : wordList) list of words
# Output     : (@list of string: ret[0]) containing general features + comparitive features
#             (@list of string: ret[1]) general features
def wordnetModule(wordList):
    threshold = 0.1  # if 20 percent of words are similar to a word then it is considered
    filtered = []  # list without outliers

    temp = []
    outliers = []
    for i in wordList:
        if len(wn.synsets(i, 'n')) != 0:
            temp.append(i)
        else:
            outliers.append(i)
    wordList = temp
    # determine outliers, by calculating how many words are similar to given word
    for word in wordList:
        temp = wordSimilarity(word, wordList)
        if temp[2] / len(wordList) >= threshold:
            filtered.append(temp)

    # determine general or common features
    generalFeature = []
    general_feature_threshold = 0.1  # if 20 percent features in document are children of any feature then it is general feature
    # check how many childrens does a word have
    for temp in filtered:
        child = countChild(temp[1], filtered)
        if child / len(wordList) >= general_feature_threshold:
            generalFeature.append([temp[0], child])

    AWList = {'coincide','collapse','colleague','commence','comment','commission','commit','commodity','communicate','community','compatible','compensate','compile','complement','complex','component','compound','comprehensive','comprise','compute','conceive','concentrate','concept','conclude','concurrent','conduct','confer','confine','confirm','conflict','conform','consent','consequent','considerable','consist','constant','constitute','constrain','construct','abandon','abstract','academy','access','accommodate','accompany','accumulate','accurate','achieve','acknowledge','acquire','adapt','adequate','adjacent','adjust','administrate','adult','advocate','affect','aggregate','aid','albeit','allocate','alter','alternative','ambiguous','amend','analogy','analyse','annual','anticipate','apparent','append','appreciate','approach','appropriate','approximate','arbitrary','area','aspect','assemble','assess','assign','assist','assume','assure','attach','attain','attitude','attribute','author','authority','automate','available','aware','behalf','benefit','bias','bond','brief','bulk','capable','capacity','category','cease','challenge','channel','chapter','chart','chemical','circumstance','cite','civil','clarify','classic','clause','code','coherent','document','domain','domestic','dominate','draft','drama','duration','dynamic','economy','edit','element','eliminate','emerge','emphasis','empirical','enable','encounter','energy','enforce','enhance','enormous','ensure','entity','environment','equate','equip','equivalent','erode','error','establish','estate','estimate','ethic','ethnic','evaluate','eventual','evident','evolve','exceed','exclude','exhibit','expand','expert','explicit','exploit','export','expose','external','extract','facilitate','factor','feature','federal','fee','file','final','finance','finite','flexible','fluctuate','focus','format','formula','forthcoming','foundation','found','framework','function','fund','fundamental','furthermore','gender','generate','generation','globe','goal','grade','grant','guarantee','guideline','hence','hierarchy','highlight','hypothesis','identical','identify','ideology','ignorance','illustrate','image','immigrate','impact','implement','implicate','implicit','imply','impose','incentive','incidence','incline','income','incorporate','index','indicate','individual','induce','inevitable','infer','infrastructure','inherent','inhibit','initial','initiate','injure','innovate','input','consult','consume','contact','contemporary','context','contract','contradict','contrary','contrast','contribute','controversy','convene','converse','convert','convince','cooperate','coordinate','core','corporate','correspond','couple','create','credit','criteria','crucial','culture','currency','cycle','data','debate','decade','decline','deduce','define','definite','demonstrate','denote','deny','depress','derive','design','despite','detect','deviate','device','devote','differentiate','dimension','diminish','discrete','discriminate','displace','display','dispose','distinct','distort','distribute','diverse','minimise','minimum','ministry','minor','mode','modify','monitor','motive','mutual','negate','network','neutral','nevertheless','nonetheless','norm','normal','notion','notwithstanding','nuclear','objective','obtain','obvious','occupy','occur','odd','offset','ongoing','option','orient','outcome','output','overall','overlap','overseas','panel','paradigm','paragraph','parallel','parameter','participate','partner','passive','perceive','percent','period','persist','perspective','phase','phenomenon','philosophy','physical','plus','policy','portion','pose','positive','potential','practitioner','insert','insight','inspect','instance','institute','instruct','integral','integrate','integrity','intelligence','intense','interact','intermediate','internal','interpret','interval','intervene','intrinsic','invest','investigate','invoke','involve','isolate','issue','item','job','journal','justify','label','labour','layer','lecture','legal','legislate','levy','liberal','licence','likewise','link','locate','logic','maintain','major','manipulate','manual','margin','mature','maximise','mechanism','media','mediate','medical','medium','mental','method','migrate','military','minimal','precede','precise','predict','predominant','preliminary','presume','previous','primary','prime','principal','principle','prior','priority','proceed','process','professional','prohibit','project','promote','proportion','prospect','protocol','psychology','publication','publish','purchase','pursue','qualitative','quote','radical','random','range','ratio','rational','react','recover','refine','regime','region','register','regulate','reinforce','reject','relax','release','relevant','reluctance','rely','remove','require','research','reside','resolve','resource','respond','restore','restrain','restrict','thesis','topic','trace','tradition','transfer','transform','transit','transmit','transport','trend','trigger','ultimate','undergo','underlie','undertake','uniform','unify','unique','utilise','valid','vary','vehicle','version','via','violate','virtual','visible','vision','visual','volume','voluntary','welfare','whereas','whereby','widespread','retain','reveal','revenue','reverse','revise','revolution','rigid','role','route','scenario','schedule','scheme','scope','section','sector','secure','seek','select','sequence','series','sex','shift','significant','similar','simulate','site','so-called','sole','somewhat','source','specific','specify','sphere','stable','statistic','status','straightforward','strategy','stress','structure','style','submit','subordinate','subsequent','subsidy','substitute','successor','sufficient','sum','summary','supplement','survey','survive','suspend','sustain','symbol','tape','target','task','team','technical','technique','technology','temporary','tense','terminate','text','theme','theory','thereby'}
    gen_and_comp_features = [x[0] for x in filtered]+outliers
    generalFeature =  [x[0] for x in generalFeature]
    gen_and_comp_features = [x for x in gen_and_comp_features if x not in AWList]
    return gen_and_comp_features,generalFeature

def calculate_score(list1, list2):
    score1 = {}  # list without outliers
    score2 = {}
    temp = []
    for i in list1:
        if len(wn.synsets(i, 'n')) != 0:
            temp.append(i)
    list1 = temp
    temp = []
    for i in list2:
        if len(wn.synsets(i, 'n')) != 0:
            temp.append(i)
    list2 = temp

    # determine outliers, by calculating how many words are similar to given word
    for word in list1:
        temp = wordSimilarity(word, list2)
        score1[word] = temp[2]
    for word in list2:
        temp = wordSimilarity(word, list1)
        score2[word] = temp[2]
    return score1,score2

def test():
    wordList = ['dog', 'cat', 'domestic', 'goa', 'mammal', 'car', 'animal', 'pet']
    print(wordnetModule(wordList))
