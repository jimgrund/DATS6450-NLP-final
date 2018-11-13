#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 12:30:44 2018

@author: varsha
"""

## ENVIRONMENT PREP
import os

import pandas as pd
from afinn import Afinn
afinn = Afinn()

import inspect
def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

### Provide the path here
# Test if this is Akash path
if ( os.path.exists("C:\\Users\\akash") ):
    os.chdir('C:\\Users\\akash\\Desktop\\GWU\\6450_NLP_SKunath\\project_one\\varsha')
    df = pd.read_csv('C:\\Users\\akash\\Desktop\\GWU\\6450_NLP_SKunath\\project_one\\varsha\\Twitter_Data.csv')
# Test if this is Jim path
if ( os.path.exists("/Users/jimgrund") ):
    os.chdir('/Users/jimgrund/Documents/GWU/NLP/final/test2/DATS6450-NLP-final/')
    df = pd.read_csv('/Users/jimgrund/Documents/GWU/NLP/final/test2/DATS6450-NLP-final/Twitter_Data.csv')
# Test if this is Varsha path
if ( os.path.exists("/Users/varsha") ):
    os.chdir('/Users/varsha/.spyder-py3/')
    df = pd.read_csv('/Users/varsha/.spyder-py3/Twitter_Data.csv')

import pandas as pd
from afinn import Afinn
afinn = Afinn()




# Sentiment analysis with AFINN
afinn = Afinn(emoticons=True)
afinn_scores = [afinn.score(text) for text in df.Text]
df['afinn'] = afinn_scores


#compute sentiment scores (polarity) and labels
sentiment_scores = [afinn.score(text) for text in df.Text]
sentiment_category = ['positive' if score > 0 
                          else 'negative' if score < 0 
                              else 'neutral' 
                                  for score in sentiment_scores]



df1 = pd.DataFrame([list(df['Text']), sentiment_scores, sentiment_category]).T
df1.columns = ['Text', 'sentiment_scores', 'sentiment_category']
df1['sentiment_scores'] = df1.sentiment_scores.astype('float')
df1.groupby(by=['Text']).describe()



