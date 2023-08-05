from Classify_word import classify_similars

#input your combined_dict
#combined_dict = classify_similars(r'C:\Users\DELL\Desktop\RoomCorpus\Important_Noun.xlsx',r'C:\Users\DELL\Desktop\RoomName','Sheet1',0.88)

location_dict={'internal':['internal', 'indoor', 'inside','in','interior'],'external':['external','exterior','outside','out'],}
size_dict={'large':['big','large']}
relation_dict={'attached':['nearby','attached']}
ordinal_dict={'premium':['important','prem','premium','first','primary'],'secondary':['secondary','supplement']}
#other words.... 

property_function={'moisture_resistant':['toilet','ceiling']}
#property_sector={'Staium':['xxx']}

class Custom_corpus:
    def __init__(self,sector,function,description,ownership):
        self.sector = sector
        self.function = function
        self.description = description
    
    def sector(input_sector): 
        input_sector.lower()    
        input_sector.capitalize()
        return('Sector_'+input_sector)
          
    def description(input_descript,location_dict,size_dict,relation_dict,ordinal_dict): #allow for multiple input 
        location = Custom_corpus.find_key(input_descript,location_dict)
        size = Custom_corpus.find_key(input_descript,size_dict)
        relation = Custom_corpus.find_key(input_descript,relation_dict)
        ordinal = Custom_corpus.find_key(input_descript,ordinal_dict)
        if location:
            return('Location_'+location)
        elif size:
            return('Size_'+location)
        elif Custom_corpus.find_key(input_descript,relation_dict):
            return('Relation_'+relation)
        elif Custom_corpus.find_key(input_descript,ordinal_dict):
            return('Ordinal_'+ordinal)

    def ownership(input_ownership):
        nn = input_ownership.lower()
        N = nn.capitalize() 
        return ('Ownership_'+N)

    def find_key(inputvalue,dictionary):
        out=str()
        for k,v in dictionary.items():
            for n in v:
                if n==inputvalue:
                    out=k
        return out
    

def room_property(function,property_function):
    proper = Custom_corpus.determ_descri(function,property_function)
    if proper:
        return('Property:'+proper)
    
def descript_corpus():
    descript_dict = []
    dicts = [location_dict,size_dict,relation_dict,ordinal_dict]
    for d in dicts:
        for k, v in d.items():  # d.items() in Python 3+
            for n in v:
                descript_dict.append(n)
                descript_dict.append(k)
    return(list(set(descript_dict)))

def standarlized_output(Function,input_descript,sector,input_ownership,combined_dict):
    func=Custom_corpus.find_key(Function,combined_dict)
    FUNCTION = str('Function_'+func)
    sec = Custom_corpus.sector(sector)
    descript= Custom_corpus.description(input_descript,location_dict,size_dict,relation_dict,ordinal_dict)
    owner = Custom_corpus.ownership(input_ownership)
    proper= str('Property:'+Custom_corpus.find_key(func,property_function))
    
    return(FUNCTION,descript,sec,owner,proper)

        
#print(standarlized_output('toilet','iner','stadium','aa',combined_dict))
        
#description has some error 
#input prem output external???
