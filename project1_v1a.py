#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 12:59:51 2018

@author: akash
"""
## ENVIRONMENT PREP
import os
import inspect

### Constants

data_directory = "data/"                                                        # Where to store data files

LIMIT = 30                                                                      # Set the limit for number of articles to download        

MAXPROCESSES = 4                                                                # Set the maximum number of processes that can run simultaneous
                                                                                # This should be less than the number of CPU Cores 

candidates_list = ['nelson','scott','heller','rosen','mccaskill','hawley']      # List of candidates we are most interested in

### Paths

if ( os.path.exists("C:\\Users\\akash") ):
    os.chdir('C:\\Users\\akash\\Desktop\\GWU\\6450_NLP_SKunath\\project_one')   # Test if this is Akash path
if ( os.path.exists("/Users/jimgrund") ):
    os.chdir('/Users/jimgrund/Documents/GWU/NLP/final/test2/DATS6450-NLP-final/') # Test if this is Jim path
if ( os.path.exists("/Users/varsha") ):
    os.chdir('/Users/varsha/.spyder-py3/')                                      # Test if this is Varsha path


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

### Sanitize Filename                                                
def sanitize_string(text):                                                      # Remove funkiness from string of text for use in filename
    text = re.sub(r"[^\w\s]", '', text)                                         # Remove all non-word characters (everything except numbers and letters)
    text = re.sub(r"\s+", '_', text)                                            # Replace all runs of whitespace with underscore
    return text

################################################################################

### Filename Construction 
def article_filename(article_title,article_source):                             # Construct filename for storing article locally on disk
    article_title = sanitize_string(article_title)
    filename = article_source + "--" + article_title + ".txt"
    return(filename)


################################################################################

### Print() Current Line    
def lineno():                                                                   # Displays what line you are working on
    return inspect.currentframe().f_back.f_lineno                               # Useful for debugging purposes

################################################################################

### Article Parser
def read_article(content, company):                                             
    try:                                                                        
        content.download()
        content.parse()
        content.nlp()
        # print("Keywords:")
        content_keywords = content.keywords
        if len(set(content_keywords) & set(candidates_list)) == 0:
            # print("content_keywords has no match for anyone in candidates_list")
            return(None)
        # print(content.keywords)
        # print(content.summary)
        print(article_filename(content.title, company))
    except Exception as e:                                                      # If no exception occurs, then continue running formula
        print(e)
        print("continuing...")
        return(None)
    article = {}                                                                # Initalize the Article index
    article['title'] = content.title
    article['text'] = content.text
    article['link'] = content.url
    #article['published'] = content.publish_date.isoformat()
    filehandle = open(data_directory + article_filename(content.title, company), 'w') # Constructs an unique naming convention
    print(content.url, file=filehandle)
    print(content.title, file=filehandle)
    print(content.text, file=filehandle)
    filehandle.close()
    return(article)
print('test:',lineno())

################################################################################

### HTML Link Parser (Part I)
def get_the_soup(source_link):
    links = []
    page = requests.get(source_link)
    for link in BeautifulSoup(page.content, 'html.parser', parse_only=SoupStrainer('a')):
        if link.has_attr('href'):                                               # Attempts to located the links found in a HTML page
            found_link = validate_and_correct_link(source_link,link['href'])
            if ( found_link == '' ):
                continue
            links.append(found_link)
    return(links)
print('test:',lineno())

################################################################################

### HTML Link Parser (Part II)
def url_has_uri(link):
    url = urllib.parse.urlparse(link)
    if len(url.path) > 1:
        return True
    return False

################################################################################
    
### Validation of Link
def validate_and_correct_link(source,link):                                     # Take the link and if it's not a full/valid URL, then update to match the source info
    url_source = urllib.parse.urlparse(source)                                  # For Example: link = "/politics/florida_democrats_furious"
    url_dest = urllib.parse.urlparse(link)                                      # Source = "https://www.huffingtonpost.com/politics"
                                                                                # Update link with the "https://www.huffingtonpost.com/" parts from source
    slash = '/'                                                                 # Only insert a slash into the url if it's needed
    if len(link) > 0 and link[0] == '/':                                        # If uri/link begin with a slash, then do not inject a new one
        slash = ''
    if url_source.netloc[len(url_source.netloc)-1] == '/':                      # If netlocs end with a slash, then do not inject
        slash = ''
    if len(url_dest.scheme) == 0 and len(url_dest.netloc) == 0:
        return(url_source.scheme + '://' + url_source.netloc + slash + link)
    if url_source.scheme != url_dest.scheme or url_source.netloc != url_dest.netloc:
        return('')
    return(link)
print('test:',lineno())

################################################################################

### Article Downloader
def get_articles_for_company(company,value):
    print("Building site for ", company)

    count = 1                                                                   # Initialize the count of articles at 1, should end with the LIMIT set above
    paper = newspaper.build(value['link'], memoize_articles=False)              # Uses python's NEWSPAPER library to extract articles
    newsPaper = {
        "link": value['link'],
        "articles": []
    }
    f = open(data_directory + 'summary_articles-' + company + '.txt', 'w')      # Creates and opens a blank text file
    print("Checking link: ", value['link'])
    if url_has_uri(value['link']):
        article_links = get_the_soup(value['link'])
        for article_link in article_links:
            if count > LIMIT:                                                   # Creates a stop if the set number of articles is reached
                break
            content = Article(article_link, request_timeout=30, fetch_images=False, MAX_KEYWORDS=100, MAX_TEXT=300000)
            article = read_article(content, company)
            if (article == None):
                # print("article skip")
                continue
            newsPaper['articles'].append(article)
            print(count, "articles downloaded from", company, " using newspaper, url: ", content.url)
            print(count, "articles downloaded from", company, " using newspaper, url: ", content.url, file=f) # Exports out to TXT file
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
print('test:',lineno())

################################################################################

data = {}                                                                       # Creates an empty array
data['newspapers'] = {}                                                         # Creates an index for the empty array


################################################################################

### Json Input
with open('NewsPapers_v1a.json') as data_file:                                  # Loads the JSON files with news sites
    companies = json.load(data_file)
print('test:',lineno())

################################################################################

### Parallelization

#f = open(data_directory + 'summary_articles.txt', 'w')

pool = mp.Pool(processes=MAXPROCESSES)                                          # Uses number of processors set above  
results = [pool.apply_async(get_articles_for_company, args=(company,value)) for company, value in companies.items()]
output = [p.get() for p in results]

data = output

################################################################################

### Saves Results

try:                                                                            # Saves the articles as a JSON-file
    if not os.path.isdir(data_directory) and not os.path.exists(data_directory): # If data_directory does not exist, then create it
        os.makedirs(data_directory)
    with open(data_directory + 'scraped_articles.json', 'w') as outfile:
        json.dump(data, outfile)
    with open(data_directory + 'scraped_articles.txt', 'w') as outfile:
        json.dump(data,outfile)
except Exception as e: print(e)
print('test:',lineno())

################################################################################

### Creates Summary

jsonTitle = data_directory + "scraped_articles.json"

def dataLoad():
    with open(jsonTitle) as f:                                                  # Loads XML file from local to Python
        pyDict = json.load(f)
    return(pyDict)

pyDict = dataLoad()                                                             # Driver 

print("\n pyDict","(",jsonTitle,"):","\n")                                      # Formats
#print(pyDict)
print('test:',lineno())

################################################################################

