#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 12:59:51 2018

@author: akash
"""
## ENVIRONMENT PREP
import os

################################################################################
# Constants:
# where to store data files
data_directory = "data/"

# Set the limit for number of articles to download
LIMIT = 8

# candidates
candidates_list = ['nelson','scott','heller','rosen','mccaskill','hawley']
################################################################################

### Provide the path here
# Test if this is Akash path
if ( os.path.exists("C:\\Users\\akash") ):
    os.chdir('C:\\Users\\akash\\Desktop\\GWU\\6450_NLP_SKunath\\project_one')
# Test if this is Jim path
if ( os.path.exists("/Users/jimgrund") ):
    os.chdir('/Users/jimgrund/Documents/GWU/NLP/final/test2/DATS6450-NLP-final/')

# https://holwech.github.io/blog/Automatic-news-scraper/


import inspect
### Basic Packages

import multiprocessing as mp
import feedparser as fp
import json
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup, SoupStrainer
import newspaper
from newspaper import Article
from time import mktime
from datetime import datetime
import urllib.parse

################################################################################
# remove funkiness from string of text for use in filename
def sanitize_string(text):
    # Remove all non-word characters (everything except numbers and letters)
    text = re.sub(r"[^\w\s]", '', text)

    # Replace all runs of whitespace with underscore
    text = re.sub(r"\s+", '_', text)

    return text


################################################################################
# construct filename for storing article locally on disk
def article_filename(article_title,article_source):
    article_title = sanitize_string(article_title)
    filename = article_source + "--" + article_title + ".txt"
    return(filename)


################################################################################
def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

################################################################################
def read_article(content, company):
    try:
        content.download()
        content.parse()
        content.nlp()
        # print("######################")
        # print("Keywords:")
        content_keywords = content.keywords
        if len(set(content_keywords) & set(candidates_list)) == 0:
            # print("content_keywords has no match for anyone in candidates_list")
            return(None)
        # print(content.keywords)
        # print(content.summary)
        # print("######################")
        print(article_filename(content.title, company))
    except Exception as e:
        print(e)
        print("continuing...")
        return(None)
    article = {}
    article['title'] = content.title
    article['text'] = content.text
    article['link'] = content.url
    #article['published'] = content.publish_date.isoformat()
    filehandle = open(data_directory + article_filename(content.title, company), 'w')
    print(content.url, file=filehandle)
    print(content.title, file=filehandle)
    print(content.text, file=filehandle)
    filehandle.close()
    return(article)

################################################################################
def get_the_soup(source_link):
    links = []
    page = requests.get(source_link)
    for link in BeautifulSoup(page.content, 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('href'):
            found_link = validate_and_correct_link(source_link,link['href'])
            if ( found_link == '' ):
                continue
            links.append(found_link)
    return(links)

################################################################################
def url_has_uri(link):
    url = urllib.parse.urlparse(link)
    if len(url.path) > 1:
        return True
    return False

################################################################################
# take the link and if it's not a full/valid URL, then update to match the source info
# ie: link = "/politics/florida_democrats_furious"
#     source = "https://www.huffingtonpost.com/politics"
#     update link with the "https://www.huffingtonpost.com/" parts from source
def validate_and_correct_link(source,link):
    url_source = urllib.parse.urlparse(source)
    url_dest = urllib.parse.urlparse(link)
    if len(url_dest.scheme) == 0 and len(url_dest.netloc) == 0:
        return(url_source.scheme + '://' + url_source.netloc + '/' + link)
    if url_source.scheme != url_dest.scheme or url_source.netloc != url_dest.netloc:
        return('')
    return(link)


################################################################################
def get_articles_for_company(company,value):
    print("Building site for ", company)

    # initialize counter for tracking number of articles per company
    count = 1

    paper = newspaper.build(value['link'], memoize_articles=False)
    newsPaper = {
        "link": value['link'],
        "articles": []
    }
    f = open(data_directory + 'summary_articles-' + company + '.txt', 'w')
    print("Checking link: ", value['link'])
    if url_has_uri(value['link']):
        article_links = get_the_soup(value['link'])
        for article_link in article_links:
            if count > LIMIT:
                break
            content = Article(article_link)
            article = read_article(content, company)
            if (article == None):
                # print("article skip")
                continue
            newsPaper['articles'].append(article)
            print(count, "articles downloaded from", company, " using newspaper, url: ", content.url)
            print(count, "articles downloaded from", company, " using newspaper, url: ", content.url, file=f)
            count = count + 1
    else:
        for content in paper.articles:
            if count > LIMIT:
                break
            article = read_article(content, company)
            newsPaper['articles'].append(article)
            print(count, "articles downloaded from", company, " using newspaper, url: ", content.url)
            print(count, "articles downloaded from", company, " using newspaper, url: ", content.url, file=f)
            count = count + 1

    count = 1
    data['newspapers'][company] = newsPaper
    f.close()
    return data

################################################################################

data = {}
data['newspapers'] = {}

################################################################################

# Loads the JSON files with news sites
with open('NewsPapers_v1a.json') as data_file:
    companies = json.load(data_file)

print('test:',lineno())

################################################################################

#f = open(data_directory + 'summary_articles.txt', 'w')

# Paralellize for each news company
pool = mp.Pool(processes=6)
results = [pool.apply_async(get_articles_for_company, args=(company,value)) for company, value in companies.items()]
output = [p.get() for p in results]

data = output

# Finally it saves the articles as a JSON-file.
try:
    # if data_directory does not exist, create it
    if not os.path.isdir(data_directory) and not os.path.exists(data_directory):
        os.makedirs(data_directory)

    with open(data_directory + 'scraped_articles.json', 'w') as outfile:
        json.dump(data, outfile)
    with open(data_directory + 'scraped_articles.txt', 'w') as outfile:
        json.dump(data,outfile)
except Exception as e: print(e)

print('test:',lineno())

################################################################################

# Input
jsonTitle = data_directory + "scraped_articles.json"

# Solution
###
def dataLoad():
    """Loads and .XML file from local to Python"""
    with open(jsonTitle) as f:
        pyDict = json.load(f)
    return(pyDict)

# Driver
pyDict = dataLoad()

print("\n pyDict","(",jsonTitle,"):","\n")
#print(pyDict)

print('test:',lineno())

################################################################################

