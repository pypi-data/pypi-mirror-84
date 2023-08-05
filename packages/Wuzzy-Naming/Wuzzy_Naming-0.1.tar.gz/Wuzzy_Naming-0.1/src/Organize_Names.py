import os
import pandas as pd
import numpy
from array import *
import string
import re 
import string 
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction import text 
from sklearn.feature_extraction.text import CountVectorizer
import itertools
from itertools import compress,islice


def import_file(FolderPath,SheetName): #file = excel, filepath=r'C:\Users\xxx\xxx\...' SheetName='Sheet1'
    os.chdir(FolderPath.strip('\u202a'))
    files = os.listdir(FolderPath)
    Input_file =  pd.DataFrame()
    for f in files:
        names = pd.read_excel(f,SheetName)
        Input_file = Input_file.append(names)
    return Input_file

def clean_text_round1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = re.sub('\w*\d\w*', '', str(text))
    return text

def max_index(lst):
    for i in lst:
        if str(i).isdigit():
            lst.append(i)
            
    max_val = max(lst)
    max_idx = lst.index(max_val)
    return max_idx

def Remove_nan(lst):
    lists=[]
    for i in lst:
        for n in i:
            if str(n) != 'nan':
                lists.append(n)
    return list(set(lists))

def Remov_Num(string):
    for i in string:
        if num.isdigit():
            if len(num)<3:
                return i

def Remove_strNum(NameFile): #input files, remove num in strings
    array_name = NameFile.values
    list_name = array_name.tolist()
    RoomNames=Remove_nan(list_name)
    RoomName_nonumber=[]
    for w in RoomNames:
        if bool(re.search(r'\d', str(w))):
            output = re.sub(r'\d+', '', str(w))
            RoomName_nonumber.append(output)
        else:
            RoomName_nonumber.append(w)
    return RoomName_nonumber

def Extract_puncut(lst): 
    lists=[]
    regex = re.compile('[@_!#$%^&*()<>?/\|}{~:+-.]') 

    for w in lst:
        if(regex.search(w) != None): 
            lists.append(w)
    return list(set(lists))

#Deal with Punctuation
def Puncuation_class(lst): 
    hyphen=[]
    hyphen_re = re.compile('-') 

    indexs=[]
    replaces=[]
    bracket=[]
    for i in range(len(lst)):
        if(re.search('\(([^)]+)', lst[i])) :
            bracket.append(re.search('\(([^)]+)', lst[i]).group(1)) #Words inside brackets
            replaces.append(lst[i].replace('('+re.search('\(([^)]+)', lst[i]).group(1)+')',''))
            indexs.append(i)
  
    for i in range(len(indexs)):
        lst[indexs[i]]=replaces[i]
    
    #Split word with - / 
    lists=[]
    hyphens=[]
    indexs_hy=[]
    replaces_hy=[]
    for w in lst:
        if(re.search('-',w)or re.search('/',w)):
            ww = w.replace('-','')
            www = ww.replace('/','')
            replaces_hy.append(www)
            indexs_hy.append(lst.index(w))
    for i in range(len(indexs_hy)):
        lst[indexs_hy[i]]=replaces_hy[i]   
    
    abbr=[]
    brackets=[]
    for b in bracket:
        if len(b)<4:
            abbr.append(b)
        else:
            brackets.append(b)  
    
    lists=[]
    for i in lst:
        if not re.search('-',i):
            lists.append(i)
        else:
            slash=i.replace(' - ','')
            add = i.replace('+','')
            lists.append(add)
    
    LST=[]
    for i in lists:
        if re.search('.',i):
            i = re.split("\.\s+", i)
            for n in i:
                if len(n.strip())<8:
                    abbr.append(n)
                else:
                    LST.append(n)
        else:
            LST.append(i)
            
    Lists=[]
    for i in LST:
        if not re.search('&',i):
            Lists.append(i)
        elif re.search('&',i) and len(i)>10:
            Lists.append(i.replace('&',''))
        elif not re.search('\w&\w',i):
            continue
        else:
            abbr.append(i)
    
    for b in brackets:
        if re.search('-/&.+-()',b):
            abbr.append(b)
        elif re.search('.',b):
            b = re.split("\.\s+", b)
            for n in b:
                if len(n.strip())<8:
                    abbr.append(n)
                else:
                    Lists.append(n)
    #clean all punctuation:
    List=[]            
    for i in Lists:
        List.append(i.translate(str.maketrans('', '', string.punctuation)))

    List = list(set(List))
    #brackets = list(set(brackets))
    abbr = list(set(abbr))
    return(List,abbr)
    #return lists

def word_ID(wordlst):
    words = wordlst
    pos_all = dict()
    
    for w in words:
        pos_l = set()
        for tmp in wn.synsets(w):
            pos_l.add(tmp.pos())
        pos_all[w] = pos_l
    ID=[]
    for Word,identity in pos_all.items():
        if identity !=set():
            identity = re.sub(r'[^\w\s]','',str(identity))
            ID.append(identity)
    return ID,pos_all

def Clean_Word(RoomName_nonumber):
    Room_abbreviation=[x for x in RoomName_nonumber if len(x)<6]
    Room_punct=Extract_puncut(RoomName_nonumber)
    Room_punctuation=list(set([x for x in Room_punct if x not in Room_abbreviation]))

    and_punct=re.compile('&')
    for i in Room_punctuation:
        if and_punct.search(i) != None and len(i)<8:
            Room_abbreviation.append(i)

    Room_abbreviation= list(set(Room_abbreviation))        
    Roomname = Puncuation_class(Room_punctuation)
    Abbr = Roomname [1]
    Normal_lst=Roomname [0]
    
    for a in Abbr:
        Room_abbreviation.append(a)
    
    Room_abbr=[]
    for r in Room_abbreviation:
        if not wn.synsets(r):
            Room_abbr.append(r)
        else:
            RoomName_nonumber.append(r)

    Room_abbr = list(set([i.strip() for i in Room_abbr]))
                            
    for n in Normal_lst:
        RoomName_nonumber.append(n)

    RoomName_nonumber=list(set(RoomName_nonumber))    
    RoomName_clean=[x for x in RoomName_nonumber if x not in Extract_puncut(RoomName_nonumber)]
    for i in Normal_lst:
        RoomName_clean.append(Normal_lst)
    return(RoomName_clean,Room_abbr)

def Valuable_word(RoomName_clean,fre_rank): #word frequency = the rank of word-freqency
    keys =[1]
    values = '.'.join(str(word) for word in RoomName_clean)
    dictionary = dict(zip(keys, values))
    df_dtm = pd.DataFrame({'Room_Name': values },{'frequency':1})
    cv = CountVectorizer(stop_words='english') #count vectorizer 

    data_cv = cv.fit_transform(df_dtm.Room_Name)
    data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
    data_dtm.index = df_dtm.index
    data_dtm.transpose()

    top_dict = {}
    for c in data_dtm.columns:
        top = data_dtm[c].sort_values(ascending=False).head(fre_rank) #排序后找到前30的top words
        top_dict[c]= list(zip(top.index, top.values))

    fre=[]
    for key, value in top_dict.items():
        for i in value:
            fre.append(i[1])
            
    index_lst = list(compress(range(len(fre)), fre)) #a quicker way for searching the INDEX
    val_words=[]
    keys = list(top_dict.keys())

    for i in index_lst:
        val_words.append(keys[i]) 
    val_words = list(set(val_words))
    return(val_words)

def Word_Classfication(val_words):#divide word based on identity 
    nouns=[]
    adj=[]
    verbs=[]
    adv=[]
    pos_all = word_ID(val_words)[1]
    ID = word_ID(val_words)[0]
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
            
    intersect_NA=set.intersection(set(nouns), set(adj)) 
    intersect_NV =set.intersection(set(nouns),set(verbs))

    nouns = list(set(nouns))
    adj = list(set(adj))
    verbs = list(set(verbs))
    adv = list(set(adv))
    return(nouns,adj,verbs,adv)

def word_class(filepath,SheetNum,fre_rank):
    NameFile=import_file(filepath,SheetNum)
    RoomName_nonumber = Remove_strNum(NameFile)
    RoomName_clean = Clean_Word(RoomName_nonumber)[0]
    val_words= Valuable_word(RoomName_clean,fre_rank) #760 frequency_rank
    nouns =  Word_Classfication(val_words)[0]
    return nouns

def Get_SynonymSet(lst):
    wordlist=lst
    synsets=[]

    for w in wordlist:
        SYN = wn.synsets(w)
        synsets.append(SYN)

    length_syn=[]
    for s in synsets:
        length = len(s)
        length_syn.append(length)

    SYNS = []
    HYPONYM=[]
    for s in synsets:
        for n in s:    
            SYNS.append(n.lemma_names())
            HYPONYM.append(n.hyponyms())

    SYN=[]
    len_syns=[]
    for s in SYNS:
        SYN.append(s)
        len_syns.append(len(s))

    len_synsets=[]
    for i in synsets:
        len_synsets.append(len(i))
    
    it = iter(len_syns)
    length_syns = [list(islice(it, 0, i)) for i in len_synsets]
    sum_lengSyn =list(map(sum, length_syns))

    Syns=[]
    for s in SYNS:
        for n in s:
            Syns.append(n)
    
    it = iter(Syns)
    Synos = [list(set(islice(it, 0, i))) for i in sum_lengSyn]
    Hyponyms=[]
    length_hypo=[]
    for h in HYPONYM:
        length_hypo.append(len(h))
        for n in h:
            Hyponyms.append(n.lemma_names())

    it_hypo= iter(length_hypo)
    length_Hypo = [list(islice(it_hypo, 0, i)) for i in len_synsets]
    sum_lengHypo=list(map(sum, length_Hypo))


    it = iter(Hyponyms)
    value_list = [list(itertools.islice(it, n)) for n in sum_lengHypo] #用 itertools.islice (list, number)

    lists=[]
    Length=[]
    length=[]
    for i in value_list:
        Length.append(len(i))
        for n in i:
            length.append(len(n))
            for h in n:
                lists.append(h)          

    it = iter(length)
    leng = [list(islice(it, 0, i)) for i in Length]
    sum_leng =list(map(sum, leng))

    hypo=[]
    for h in Hyponyms:
        for n in h:
            hypo.append(n)
        
    it = iter(hypo)
    Hypos = [list(set(islice(it, 0, i))) for i in sum_leng]

    for i in range(len(Hypos)):
        Hypos[i].extend(Synos[i])

    keys= wordlist
    values=Hypos
    dictionary = dict(zip(keys, values))
    return (dictionary) #build dictionary for all nouns

def Dict_access(dic):
    lists=[]
    for k,v in dic.items():
        lists.append(k)
        for w in v:
            lists.append(w)
    return lists

def Corpus_forSpellCorrect(noun_corpus, adv_corpus, adj_corpus, verb_corpus):
    key=['noun_n','adv_a','adj_r','verb_v']
    value=[noun_corpus, adv_corpus, adj_corpus, verb_corpus]
    corpus_dictionary = dict(zip(key, value))

    return corpus_dictionary

def Corpus_Combo(filepath,SheetNum):

    NameFiles=import_file(filepath,SheetNum)
    Name_nonum=Remove_strNum(NameFiles)
    Cleaned_name = Clean_Word(Name_nonum)[0]
    Abbreviation = Clean_Word(Name_nonum)[1]
    valuable_words = Valuable_word(Cleaned_name,760)

    nouns = Word_Classfication(valuable_words)[0]
    adj = Word_Classfication(valuable_words)[1]
    verbs = Word_Classfication(valuable_words)[2]
    adv = Word_Classfication(valuable_words)[3]

    Synsets_nouns=Get_SynonymSet(nouns)
    Synsets_adj=Get_SynonymSet(adj)
    Synsets_adv=Get_SynonymSet(adv)
    Synsets_verbs=Get_SynonymSet(verbs)

    noun_syns= Dict_access(Synsets_nouns)
    adj_syns= Dict_access(Synsets_adj)
    adv_syns=Dict_access(Synsets_adv)
    verb_syns=Dict_access(Synsets_verbs)

    Corpus = Corpus_forSpellCorrect(noun_syns,adj_syns,adv_syns,verb_syns)
    return Corpus

def Combined_words(Corpus):
    all= [v for k,v in Corpus.items()]
    all_corpus =[]
    for i in all:
        for n in i:
            all_corpus.append(n)


    return(list(set(all_corpus)))

#print(word_class(r'C:\Users\DELL\Desktop\RoomName','Sheet1',760))


#print(Corpus_Combo('C:\Users\DELL\Desktop\RoomName','Sheet1'))
#CORPUS = Corpus_Combo(r'C:\Users\DELL\Desktop\RoomName','Sheet1')
#print(CORPUS['noun_n'])

'''print ('build your custom corpus, input FilePath: ')
FilePath = input('')
print ('Now input specific sheetName of input excel file: (e.g.Sheet1)')
SheetName = input('')
custom_corpus = Corpus_Combo(FilePath,SheetName)
print ('here is your corpus:')'''
