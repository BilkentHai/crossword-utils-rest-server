from nltk.corpus import wordnet as wn
from array import array

def count_underscore(word):
    i = 0
    for l in word:
        if l == '_':
            i += 1
    return i


def get_n_length_words(n):
    words = list(wn.words())
    nLength = set()
    for word in words:
        i = count_underscore(word)
        if len(word) - i == n:
            word = word.replace('_', '')
            nLength.add(word.upper())
    return sorted(nLength)


def get_n_length_json(n):
    nLength = get_n_length_words(n)
    result = "[\n"
    i = 0
    for word in nLength:
        result = result + "{\n\"word\": \"" + word + "\",\n\"score\": 1" + "\n},\n"
    result = result[:-2]
    return result + "\n]" + "\n"