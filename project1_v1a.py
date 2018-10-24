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
LIMIT = 4
################################################################################

### Provide the path here
# Test if this is Akash path
if ( os.path.exists("C:\\Users\\akash") ):
    os.chdir('C:\\Users\\akash\\Desktop\\GWU\\6450_NLP_SKunath\\project_one') 
# Test if this is Jim path
if ( os.path.exists("/Users/jimgrund") ):
    os.chdir('/Users/jimgrund/Documents/GWU/NLP/final/DATS6450-NLP-final/') 
#os.chdir("C:\\Users\\BBCETBB\\Documents\\gwu\\6450_NLP_SKunath\\project_one")
                     
# https://holwech.github.io/blog/Automatic-news-scraper/


import inspect
### Basic Packages

import feedparser as fp
import json
import re
import newspaper
from newspaper import Article
from time import mktime
from datetime import datetime

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

data = {}
data['newspapers'] = {}

################################################################################

# Loads the JSON files with news sites
with open('NewsPapers_v1a.json') as data_file:
    companies = json.load(data_file)

print('test:',lineno())

################################################################################

count = 1
f = open(data_directory + 'summary_articles.txt', 'w')

# Iterate through each news company
for company, value in companies.items():
    # If a RSS link is provided in the JSON file, this will be the first choice.
    # Reason for this is that, RSS feeds often give more consistent and correct data.
    # If you do not want to scrape from the RSS-feed, just leave the RSS attr empty in the JSON file.
    if 'rss' in value:
        d = fp.parse(value['rss'])
        print("Downloading articles from ", company)
        newsPaper = {
            "rss": value['rss'],
            "link": value['link'],
            "articles": []
        }
        for entry in d.entries:
            # Check if publish date is provided, if no the article is skipped.
            # This is done to keep consistency in the data and to keep the script from crashing.
            if hasattr(entry, 'published'):
                if count > LIMIT:
                    break
                article = {}
                article['link'] = entry.link
                date = entry.published_parsed
                article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
                try:
                    content = Article(entry.link)
                    content.download()
                    content.parse()
                except Exception as e:
                    # If the download for some reason fails (ex. 404) the script will continue downloading
                    # the next article.
                    print(e)
                    print("continuing...")
                    continue
                article['title'] = content.title
                article['text'] = content.text
                newsPaper['articles'].append(article)
                print(count, "articles downloaded from", company, ", url: ", entry.link)
                print(count, "articles downloaded from", company, ", url: ", entry.link,file =f)
                count = count + 1
    else:
        # This is the fallback method if a RSS-feed link is not provided.
        # It uses the python newspaper library to extract articles
        print("Building site for ", company)
        paper = newspaper.build(value['link'], memoize_articles=False)
        newsPaper = {
            "link": value['link'],
            "articles": []
        }
        noneTypeCount = 0
        for content in paper.articles:
            if count > LIMIT:
                break
            try:
                content.download()
                content.parse()
                print(article_filename(content.title, company))
            except Exception as e:
                print(e)
                print("continuing...")
                continue
            # Again, for consistency, if there is no found publish date the article will be skipped.
            # After 10 downloaded articles from the same newspaper without publish date, the company will be skipped.
            if content.publish_date is None:
                print(count, " Article has date of type None...")
                noneTypeCount = noneTypeCount + 1
                if noneTypeCount > 10:
                    print("Too many noneType dates, aborting...")
                    noneTypeCount = 0
                    break
                count = count + 1
                continue
            article = {}
            article['title'] = content.title
            article['text'] = content.text
            article['link'] = content.url
            article['published'] = content.publish_date.isoformat()
            newsPaper['articles'].append(article)
            filehandle = open(data_directory + article_filename(content.title, company), 'w')
            print(content.url, file=filehandle)
            print(content.title, file=filehandle)
            print(content.text, file=filehandle)
            filehandle.close()
            print(count, "articles downloaded from", company, " using newspaper, url: ", content.url)
            print(count, "articles downloaded from", company, " using newspaper, url: ", content.url, file=f)
            count = count + 1
            noneTypeCount = 0
    count = 1
    data['newspapers'][company] = newsPaper
f.close()                   

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


