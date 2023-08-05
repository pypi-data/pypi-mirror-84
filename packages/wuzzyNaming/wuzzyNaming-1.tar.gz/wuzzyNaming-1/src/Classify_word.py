from Organize_Names import word_class, Get_SynonymSet
from nltk.corpus import wordnet as wn
import os
import pandas as pd
import itertools
import numpy
import json


#open important_noun excel file:
def open_excel(path):
    data= pd.read_excel(path,engine='xlrd')

    imp_noun = [i for i in data['Imp_noun']]
    return imp_noun

def classify_similars(imp_path,roomname_path,sheetnum,threhold): #Combine your custom words(standard name) with the built-in corpus
    imp_noun=open_excel(imp_path)
    nouns=word_class(roomname_path,sheetnum,760) 

    SYNSETS=[]
    for s in nouns:
        syn1 = wn.synsets(s)[0]
        SYNSETS.append(syn1)

    SYNSETS_imp=[]
    for i in imp_noun:
        syn2 = wn.synsets(i)
        try:
            SYNSETS_imp.append(syn2[0])
        except:
            continue

    Similarity_res=[]
    for s in SYNSETS_imp: 
        for n in SYNSETS:
            Similarity_res.append(s.wup_similarity(n)) 
        
    n= len(SYNSETS) #!!!!!
    similarity = [Similarity_res[i:i + n] for i in range(0, len(Similarity_res), n)]

    similarity_score=[]
    for s in similarity:
        for n in s:
            similarity_score.append(n)
    dictionary=dict()

    for i in range(len(similarity)):
        dictionary.setdefault(imp_noun[i],[]).append(similarity[i])
    threhold=0.88

    index=[];ind_len=[];sim=[]
    for s in similarity:
        for i in range(len(s)):
            if s[i]>threhold:
                index.append(i)
                sim.append(s[i])
            else:
                index.append(len(imp_noun)+300) #or 1000
                sim.append(0)

    n= len(SYNSETS)
    index_lst= [list(index[i:i + n]) for i in range(0, len(index), n)]

    index=[]
    for i in index_lst:
        for l in i:
            index.append(l)

    Sim_score = numpy.array(similarity_score)
    Index = numpy.array(index)
    inds = Sim_score.argsort()
    sorted_result = Index[inds]   
    sorted_result.tolist()
    result= [list(index[i:i + n]) for i in range(0, len(sorted_result), n)]

    Similar_words=[]
    indexlst = [[i for i in nested if i != 1000] for nested in result]

    for i in indexlst:
        sim=[]
        for index in i:
            sim.append(nouns[index])
        Similar_words.append(sim)

    keys=[n for n in imp_noun]
    values=Similar_words
    Dict=dict(zip(keys,values))

    standard_Dict = dict(sorted(Dict.items(), key=lambda x: x[0].lower()) )
    noun_syn=Get_SynonymSet(imp_noun)
    combined_dict = {**standard_Dict, **noun_syn}

    return combined_dict

#print(classify_similars(r'C:\Users\DELL\Desktop\RoomCorpus\Important_Noun.xlsx',r'C:\Users\DELL\Desktop\RoomName','Sheet1',0.88))

def combined_dict(important_nounPath,roomname_path,sheetNum,tolerance):
    combined_dict = classify_similars(important_nounPath,roomname_path,sheetNum,tolerance)
    return(combined_dict)


#create Build-in Combined_dict
#combined_dict = classify_similars(r'C:\Users\DELL\Desktop\RoomCorpus\Important_Noun.xlsx',r'C:\Users\DELL\Desktop\RoomName','Sheet1',0.88)
#Filename = os.path.join(r'C:\Users\DELL\Desktop\RoomCorpus','Combined_dict.txt')
#File1 = open(Filename,'w')
#File1.write(json.dumps(combined_dict,ensure_ascii=True))
#File1.close()


