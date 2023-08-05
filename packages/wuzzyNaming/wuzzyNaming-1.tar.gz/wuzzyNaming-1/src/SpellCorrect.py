#input--remove punctuation
import re
import string
import nltk
from nltk.tokenize import TweetTokenizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import wordnet as wn
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from googletrans import Translator
from textblob import TextBlob
from Organize_Names import word_ID,Corpus_Combo


#inp_words = input('')
def remove_punctuation(word): #AND remove number
    punctuation='!"#$%\'()*+,-/:;<=>?@[\\]^`{|}~'''
    remove_punct = re.sub('[%s]' % re.escape(punctuation), '',str(word))
    #remove blank space
    remove_blank = re.sub(' ','',str(remove_punct))
    result = ''.join([i for i in remove_blank if not i.isdigit()])
    return(result)
    
def tokenize_input(word): 
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)#https://www.nltk.org/api/nltk.tokenize.html
    return(tknzr.tokenize(word))

#OPTIONAL 
def stemmer(sentence):
    porter = PorterStemmer()
    token_words=word_tokenize(sentence)
    token_words
    stem_sentence=[]
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)

def fuzzy_search(word,word_list):
    RATIO=[]
    sim_result=[]
    answer=[]
    for w in word:   
        RATIO=[process.extract(w,word_list,limit=50,scorer=fuzz.ratio)] #query&choices- choices=list[]
    
    sim_result=[r[0] for r in RATIO]
    answer = [i[0]for i in sim_result]
    return answer,RATIO

def input_processing(translate, input_word, corpus):
    #TRANSLATE
    try:
        translate =='Yes'or'yes'
        language =TextBlob(input_word)
        orilan =language.detect_language()
        if(orilan !='en'):
            translator = Translator()
            result = translator.translate(input_word,src = orilan, dest = 'en') #翻译掉
            input_word=(f'{result.text}')
    except:
        input_word = input_word
        
    no_punctuation = remove_punctuation(input_word)
    tokenize = tokenize_input(no_punctuation)
    #no_stemmer = remove_stemmer(tokenize)
    fuzzy_search_result = fuzzy_search(tokenize,corpus)[0]
    for i in fuzzy_search_result:
        return i
