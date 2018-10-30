#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 28 19:19:20 2018

@author: varsha
"""
## ENVIRONMENT PREP
import os
### Provide the path here
# Test if this is Akash path
if ( os.path.exists("C:\\Users\\akash") ):
    os.chdir('C:\\Users\\akash\\Desktop\\GWU\\6450_NLP_SKunath\\project_one\\varsha')
    twitter_data = 'C:\\Users\\akash\\Desktop\\GWU\\6450_NLP_SKunath\\project_one\\varsha\\Twitter_Data.csv'
# Test if this is Jim path
if ( os.path.exists("/Users/jimgrund") ):
    os.chdir('/Users/jimgrund/Documents/GWU/NLP/final/test2/DATS6450-NLP-final/')
    twitter_data = '/Users/jimgrund/Documents/GWU/NLP/final/test2/DATS6450-NLP-final/Twitter_Data.csv'
# Test if this is Varsha path
if ( os.path.exists("/Users/varsha") ):
    os.chdir('/Users/varsha/.spyder-py3/')

## Inputs


import inspect
def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

#Commands to install the following
#conda install -c spacy spacy 
#conda install -c conda-forge pyldavis 
#python -m spacy download en
# conda install -c conda-forge/label/gcc7 pyldavis

import spacy
#spacy.load('en')
from spacy.lang.en import English

parser = English()
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens
print('start test:',lineno())


import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
print('test:',lineno())
   
    
from nltk.stem.wordnet import WordNetLemmatizer
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens
print('test:',lineno())


import random
text_data = []
with open(twitter_data, encoding = "utf8") as f:
    for line in f:
        tokens = prepare_text_for_lda(line)
        if random.random() > .99:
            #print(tokens)
            text_data.append(tokens)
print('test:',lineno())
 
           
from gensim import corpora
dictionary = corpora.Dictionary(text_data)

corpus = [dictionary.doc2bow(text) for text in text_data]
print('test:',lineno())



import pickle
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')
print('test:',lineno())


import gensim
NUM_TOPICS = 10
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model10.gensim')



topics = ldamodel.print_topics(num_words=9)
for topic in topics:
    print(topic)
print('test:',lineno())
    

new_doc = 'Practical Bayesian Optimization of Machine Learning Algorithms'
new_doc = prepare_text_for_lda(new_doc)
new_doc_bow = dictionary.doc2bow(new_doc)
print(new_doc_bow)
print(ldamodel.get_document_topics(new_doc_bow))    
print('test:',lineno())
    

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 15, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')
topics = ldamodel.print_topics(num_words=14)
for topic in topics:
    print(topic)
print('test:',lineno())
    

ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 20, id2word=dictionary, passes=15)
ldamodel.save('model20.gensim')
topics = ldamodel.print_topics(num_words=7)
for topic in topics:
    print(topic)
print('test:',lineno())


dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
corpus = pickle.load(open('corpus.pkl', 'rb'))
lda = gensim.models.ldamodel.LdaModel.load('model5.gensim')    
print('test:',lineno())


#Visuals -- use jupyter notebook
import pyLDAvis.gensim
lda_display = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics=False)
pyLDAvis.display(lda_display)

print('finish test:',lineno())
del(corpus, line, new_doc,new_doc_bow, twitter_data,topic, topics,tokens, text_data)

                