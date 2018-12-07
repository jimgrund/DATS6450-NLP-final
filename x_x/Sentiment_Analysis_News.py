# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 09:40:48 2018

@author: akash
"""
## ENVIRONMENT PREP
import os
from os import listdir
from os.path import isfile
from os.path import join
import inspect
import pandas as pd
from afinn import Afinn
afinn = Afinn()
import re
import string
import hashlib
import nltk
import glob
import errno
import csv
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import metrics
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords


### Provide the path here
# Test if this is Akash path
if ( os.path.exists("C:\\Users\\akash") ):
    os.chdir('C:\\Users\\akash\\Desktop\\GWU\\6450_NLP_SKunath\\project_one')
    directory = "C:\\Users\\akash\\Desktop\\GWU\\6450_NLP_SKunath\\project_one\\news-data"
# Test if this is Jim path
if ( os.path.exists("/Users/jimgrund") ):
    os.chdir('/Users/jimgrund/Documents/GWU/NLP/final/test2/DATS6450-NLP-final/')
    directory = "/Users/jimgrund/Documents/GWU/NLP/final/test2/DATS6450-NLP-final/news-data"
# Test if this is Varsha path
if ( os.path.exists("/Users/varsha") ):
    os.chdir('/Users/varsha/.spyder-py3/')
    directory = "/Users/varsha/.spyder-py3/news-data"
   
    
### Debugging Tool 
def lineno():                                                                   # Displays what line you are working on
    return inspect.currentframe().f_back.f_lineno                               # Useful for simple debugging purposes
print('test:',lineno())

################################################################################
article_hash = {}

files = [f for f in listdir(directory) if isfile(join(directory, f))]

for file in files:
    #file = pathlib.Path( "/Users/varsha/Python Workspace/homework_2/data")
    #print(file)
    fileop=open(directory+"/"+file,"r",encoding = "utf8")
    text = fileop.read()
    article_hash[file]  = text
    #print("-----------------------------------")
    #print("file;" , file)
    #print(article_hash[file])

################################################################################

full_text = []
article = [] 
sent_score = []
sent_category =[]

for key in article_hash.keys():
     #print("-----------------------------")
     #print("key value is :",key ) 
     #print(article_hash[key])
     text = article_hash[key]
# Sentiment analysis with AFINN
     afinn = Afinn(emoticons=True)
     afinn_scores = [afinn.score(text)]
     #print(article_hash[key])
     # print(afinn_scores)
 

     #compute sentiment scores (polarity) and labels
     sentiment_scores = [afinn.score(text)]
     sentiment_category = ['positive' if score > 0 
                                else 'negative' if score < 0 
                                    else 'neutral' 
                                        for score in sentiment_scores]

     #print(article_hash[key])
     #print(sentiment_scores)
     #print(sentiment_category)
     
     full_text.append(text)
     sent_score.append(sentiment_scores)
     sent_category.append(sentiment_category)
     
     for f in files:
         article.append(f)
################################################################################
         
df1 = pd.DataFrame([list(files),(sent_score), sent_category, full_text]).T
df1.columns = ['ArticleTitle', 'sentiment_scores', 'sentiment_category','full_text'] # Trying to make full Text a popout?
#df1['sentiment_scores'] = df1['sentiment_scores'].astype('float')               # This results in an error 
#df1.groupby(by=['ArticleTitle']).describe()




################################################################################


print('test:',lineno())
