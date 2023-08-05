from SpellCorrect import input_processing
from Organize_Names import Corpus_Combo, Combined_words,Word_Classfication,import_file,Remov_Num,Remove_nan,Remove_strNum,Clean_Word,Valuable_word
from Import_corpus import input_file
from Get_Synonyms import Get_SynonymFromlst
from Standard_corpus import standarlized_output,descript_corpus
from BuiltinAll_corpus import exportCombined,exportDict,inputDict
from Classify_word import combined_dict
from BuiltinAll_corpus import inputDict

def Function(translate,input_function,noun_list):
    input_fun=input_processing(translate,input_function,noun_list) #all_corpus--> word_list
    return (input_fun)

def Description(translate,input_description,descript_corpus): #Fu word_list
    input_description = input_processing(translate,input_description,descript_corpus)
    return(input_description)

def Archi_Sector(INPUT_sector,translate):
    sectors = inputDict(r'C:\Users\DELL\Desktop\RoomCorpus\sectors.txt')
    Sector = input_processing(translate,INPUT_sector,sectors)
    return(Sector)

def Synonym_Function(correct_function,aimlist,tolerance):
    Function = Get_SynonymFromlst(aimlist,correct_function,tolerance)
    return(Function)

def Custom_corpus(FilePath,sheetName):
    Corpus = Corpus_Combo(FilePath,sheetName)
    return(Corpus)

def Buildin_corpus():
    Corpus = inputDict(r'C:/Users/DELL/Desktop/RoomCorpus/Corpus_Combo.txt')
    all_corpus = exportCombined(r'C:\Users\DELL\Desktop\RoomCorpus','All_corpus.txt',ex_Corpus)
    return(Corpus,all_corpus)

def Custom_or_Build(build,Custom_path,Buildin_corpus,BuildinAll_corpus):
    if build=='yes':
        Custom_corpus = Corpus_Combo(Custom_path,'Sheet1')
        all_corpus = Combined_words(Custom_corpus)
        noun_lst = Custom_corpus['noun_n']
        return(Custom_corpus,all_corpus,noun_lst)

    elif build=='no':
        buildin_corpus = inputDict(Buildin_corpus)
        all_corpus = inputDict(BuildinAll_corpus)
        noun_lst = buildin_corpus['noun_n']
        return(buildin_corpus,all_corpus,noun_lst)

    else:
        return('please enter valid content: yes or no')

def standard_Dict(build,CustomNoun_path,Roomname_path,tolerance):
    if build=='yes':
        combined = combined_dict(CustomNoun_path,Roomname_path,'Sheet1',tolerance)
        return(combined)
    elif build=='no':
        combined = inputDict(r'C:\Users\DELL\Desktop\wuzzynaming\RoomName_standard\Combined_dict.txt')
        return(combined)
    else:
        return('please enter valid content: yes or no')

def Abbreviation(FilePath,sheetName):
    NameFiles=import_file(FilePath,sheetName)
    Name_nonum=Remove_strNum(NameFiles)
    Abbreviation = Clean_Word(Name_nonum)[1]  
    return(Abbreviation)

def Value_word(FilePath,sheetName,Rank):
    NameFiles=import_file(FilePath,sheetName)
    Name_nonum=Remove_strNum(NameFiles)
    Cleaned_name = Clean_Word(Name_nonum)[0]
    valuable_words = Valuable_word(Cleaned_name,Rank) 
    return(Abbreviation)

def Word_Class(valuable_words):
    nouns= Word_Classfication(valuable_words)[0]
    adj= Word_Classfication(valuable_words)[1]
    verbs= Word_Classfication(valuable_words)[2]
    adv= Word_Classfication(valuable_words)[3]
    return(nouns,adj,verbs,adv)

def standard(Function,Description,Sector,Ownership,combined_dict):
    standards = standarlized_output(Function,Description,Sector,Ownership,combined_dict)
    Function,Description,Sector,Ownership,Property = standards[0],standards[1],standards[2],standards[3],standards[4]
    return(Function,Description,Sector,Ownership,Property)

