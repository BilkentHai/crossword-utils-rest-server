import requests
from PyDictionary import PyDictionary
from nltk.corpus import wordnet as wn

def py_dic_syn( str):
    j = PyDictionary().synonym(str, "html.parser")
    s = set()
    if j:
        for syn in j[str]:
            s.add( syn)
    return s

def wn_syn( str):
    wnsynonyms = set()
    syn_sets = wn.synsets(str)
    for i, j in enumerate(syn_sets):
        for name in j.lemma_names():
            wnsynonyms.add(name)
    return wnsynonyms

def find_all_synonyms( str, l):
    synonyms = set()
    s1 = wn_syn( str)
    s2 = py_dic_syn(str)
    s3 = conceptnet_synonyms( str)
    for s in s2:
        if(len(s) == l):
           synonyms.add(s)
    for s in s1:
        if (len(s) == l):
            synonyms.add(s)
    for s in s3:
        if (len(s) == l):
            synonyms.add(s)
    if str in synonyms:
        synonyms.remove(str)
    return synonyms

def py_dic_ant( str):
    j = PyDictionary().antonym(str, "html.parser")
    a = set()
    if j:
        for ant in j[str]:
            a.add(ant)
    return a


def wn_ant( str):
    wnantonyms = set()
    syn_sets = wn.synsets(str)
    for i, j in enumerate(syn_sets):
        for name in j.lemmas():
            for ant in name.antonyms():
                wnantonyms.add(ant.name())
    return wnantonyms

def conceptnet_synonyms( str):
    obj = requests.get('http://api.conceptnet.io/c/en/' + str).json()
    s = set();

    for j in obj['edges']:
        if j['rel']['label'] == "SimilarTo":
            s.add(j['start']['label'])
    return s

def find_all_antonyms( str, l):
    antonyms = set()
    s1 = wn_ant(str)
    s2 = py_dic_ant(str)
    for s in s2:
        if (len(s) == l):
            antonyms.add(s)
    for s in s1:
        if (len(s) == l):
            antonyms.add(s)
    return antonyms