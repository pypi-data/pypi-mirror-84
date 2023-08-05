from nltk.corpus import wordnet as wn
import itertools
import re
import nltk
import SpellCorrect
from SpellCorrect import word_ID,remove_punctuation, tokenize_input

def Get_Synset(aimlst,inputword):
    synsets_aim=[]
    synsets_input=str()
    for w in aimlst:
        synsets_aim.append(wn.synsets(w))
    #for i in inputword:
        #distinguish the word type 
        #synsets_input = wordnet.synset(i +'.n.01')
    for d in word_ID(inputword):
        if re.search('n',str(d)):
            synsets_input = wn.synsets(inputword)[0]
        elif re.search('a',str(d)):
            synsets_input = wn.synsets(inputword)[0]
        elif re.search('v',):
            synsets_input = wn.synsets(inputword)[0] #wn.synset(inputword[0] +'.v.01')
        else:
            continue
    return (synsets_aim,synsets_input)
    #return synsets_input

def Get_similarity(syn_aimlst, syn_input):
    similarity=[]
    syn_sim={}
    syn=[]
    length_syn=[]
    for syns in syn_aimlst:
        length = len(syns)
        length_syn.append(length)
        for s in syns:
            similarity.append(s.wup_similarity(syn_input))
            #syn_sim[len] = s.wup_similarity(synset_input)
            syn.append(s)

    for i in range(len(syn)):
        syn_sim[syn[i]] = similarity[i]

#--------------------------------------------------------------------------------
    Similarity=[]
    for s in similarity:
        if s is None or s==None:
            Similarity.append(0)
        else:
            Similarity.append(s)

    #// Split or break a Python list into Unequal chunks, 
    it = iter(Similarity)
    value_list = [list(itertools.islice(it, n)) for n in length_syn] #用 itertools.islice (list, number)
    clean_value=[]
    for sublist in value_list:
        cleaned = [elem for elem in sublist if elem is not None]
        if len(cleaned):  # anything left?
            clean_value.append(cleaned)
        else:
            clean_value.append([0])

    sim_scores=[]

    for i in clean_value:
        sim_scores.append(max(i))

    return(sim_scores)

def Get_words(aimlst,similarity_scores,tolerance):
    #val_words = [w for w in val_words]
    index_lst=[]
    for i in range(len(similarity_scores)):
        if similarity_scores[i]>tolerance:
            index_lst.append(i)

    words = [aimlst[i] for i in index_lst]
    return(set(words))

def Get_SynonymFromlst(aimlist,inputword,tolerance):
    Synsets=[]
    similarity=[]
    words=[]
    
    Synsets= Get_Synset(aimlist,inputword)
    similarity = Get_similarity(Synsets[0], Synsets[1])
    words = Get_words(aimlist,similarity,tolerance)

    return list(set(words))
    

def Classify_words(unorganize_wordlist): #Classify the word into noun,adv,adj,verb
    nouns=[]
    adj=[]
    verbs=[]
    adv=[]
    pos_all = word_ID(unorganize_wordlist)[1]
    #ID = word_ID(unorganize_wordlist)[0]
    for word,identity in pos_all.items():
        for i in identity:
            if i=='n':
                nouns.append(word)
            elif i=='a'or i=='s':
                adj.append(word)
            elif i=='v':
                verbs.append(word)
            elif i=='r':
                adv.append(word)

    key=['noun_n','adv_a','adj_r','verb_v']
    value=[nouns, adv, adj, verbs]
    corpus_dictionary = dict(zip(key, value))
    return(corpus_dictionary)


#make sure the 'corpus' is organized with"key=['noun_n','adv_a','adj_r','verb_v']" Before input
def Get_SynResult_function(input_words,corpus,tolerance): 
    no_punctuation = remove_punctuation(input_words)
    tokenize = tokenize_input(no_punctuation)
    
    pos_all = dict()
    for w in tokenize:
        pos_l = set()
        for tmp in wn.synsets(w):
            #if tmp.name().split('.')[0] == w:
            pos_l.add(tmp.pos())
        pos_all[w] = pos_l
        
    ID=[]
    result=[]
    for word,identity in pos_all.items():
        if identity !=set():
            identity = re.sub(r'[^\w\s]','',str(identity))
            ID.append(identity)
            for d in identity:
                if re.search('n', d) :
                    result = Get_SynonymFromlst(corpus['noun_n'],input_words,tolerance)
                #'noun_n','adv_a','adj_r','verb_v'
        return(result)

def Get_SynResult_description(input_words,corpus,tolerance):  #This corpus directs to the Custom_Corpus we build for BIM object_name
    no_punctuation = remove_punctuation(input_words)
    tokenize = tokenize_input(no_punctuation)
    
    pos_all = dict()
    for w in tokenize:
        pos_l = set()
        for tmp in wn.synsets(w):
            #if tmp.name().split('.')[0] == w:
            pos_l.add(tmp.pos())
        pos_all[w] = pos_l
        
    ID=[]
    result=[]
    for word,identity in pos_all.items():
        if identity !=set():
            identity = re.sub(r'[^\w\s]','',str(identity))
            ID.append(identity)
            for d in identity:
                #'noun_n','adv_a','adj_r','verb_v'
                if re.search('a',d):
                    result = Get_SynonymFromlst(corpus['adj_r'],input_words,tolerance)
                elif re.search('v',d):
                    result = Get_SynonymFromlst(corpus['verb_v'],input_words,tolerance)
                elif re.search('r',d):
                    result = Get_SynonymFromlst(corpus['adv_a'],input_words,tolerance)
        return(result)


