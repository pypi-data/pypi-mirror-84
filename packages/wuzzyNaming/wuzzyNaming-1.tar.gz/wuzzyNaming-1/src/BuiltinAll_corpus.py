from Organize_Names import Corpus_Combo, Combined_words
import os.path
import json
from SpellCorrect import input_processing

def exportDict(export_path,name,input_path,sheetNum):  
    FileName = os.path.join(export_path,name)
    built_in = Corpus_Combo(input_path,sheetNum)
    File1 = open(FileName,'w')
    File1.write(json.dumps(built_in,ensure_ascii=True)) #use json 
    File1.close()

def exportCombined(export_path,name,corpus):  
    FileName = os.path.join(export_path,name)
    built_in = Combined_words(corpus)
    File1 = open(FileName,'w')
    File1.write(json.dumps(built_in,ensure_ascii=True)) #use json 
    File1.close()

def inputDict(input_path): #/https://blog.csdn.net/chenmozhe22/article/details/81434081
    with open(input_path,'r') as f:
        File = f.read()
        OUT = eval(File) #add eval change from string to dictionary
        return(OUT)



#Corpus_ComboDict = exportDict(r'C:\Users\DELL\Desktop\RoomCorpus','Corpus_Combo.txt',r'C:\Users\DELL\Desktop\RoomName','Sheet1')

#Corpus = Corpus_Combo(r'C:\Users\DELL\Desktop\RoomName','Sheet1')

#Combined_wordsDict = exportCombined(r'C:\Users\DELL\Desktop\RoomCorpus','All_corpus.txt',Corpus)
#ex_Combined = inputDict(r'C:/Users/DELL/Desktop/RoomCorpus/All_corpus.txt')
#ex_Corpus = inputDict(r'C:/Users/DELL/Desktop/RoomCorpus/Corpus_Combo.txt')
#error type=dictionary
