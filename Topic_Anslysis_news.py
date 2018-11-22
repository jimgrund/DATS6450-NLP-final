import pandas as pd
import nltk
import os
from nameparser.parser import HumanName
from nltk.corpus import wordnet
from os import listdir
from os.path import isfile, join

newspath = os.path.join(os.getcwd(), 'data', 'news-data')

candidates_list = ['bill nelson','rick scott','dean heller','jacky rosen','claire mccaskill','josh hawley']

def get_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)

    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):   # only look for entity type of person
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1].upper() in map(str.upper, candidates_list):      # only accept names in the candidates_list
                if name[:-1] not in person_list:
                    person_list.append(name[:-1])
            name = ''
        person = []


results_df = pd.DataFrame()

newsfiles = [f for f in listdir(newspath) if isfile(join(newspath, f))]

for file in newsfiles:
   article_df = pd.DataFrame()      # initialize dataframe for each article
   person_list = []
   person_names=person_list

   filepath = newspath + "/" + file
   data = open(filepath,'r')

   new_data = data.read()
   #print(new_data)
   get_names(new_data)
   #print(file)
   article_df['file'] = file
   #print(person_names)
   article_df['candidates'] = [person_names]
   #print("\n")
   results_df = results_df.append(article_df)

print(results_df)
