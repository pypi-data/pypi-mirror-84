import csv

def input_file(FileName): #FileName==string, csv file 
    Corpus=[]
    with open(FileName, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for n in row:
                Corpus.append(n)
    Corpus =  list(set(Corpus)) 
    return(Corpus) 