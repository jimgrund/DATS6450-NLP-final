import pandas as pd
import nltk
import os
from nameparser.parser import HumanName
from nltk.corpus import wordnet
from os import listdir
from os.path import isfile, join
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import numpy as np

np.random.seed(2018)

nltk.download('wordnet')


newspath = os.path.join(os.getcwd(), 'data', 'news-data')

candidates_list = ['bill nelson','rick scott','dean heller','jacky rosen','claire mccaskill','josh hawley']



def get_topics(text):
    def lemmatize_stemming(text):
        stemmer = SnowballStemmer("english", ignore_stopwords=True)
        return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

    def preprocess(text):
        result = []
        for token in gensim.utils.simple_preprocess(text):
            if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
                #result.append(token)
                result.append(lemmatize_stemming(token))
        return result


    words = []
    for word in text.split(' '):
        words.append(word)

    processed_data = preprocess(text)

    dictionary = gensim.corpora.Dictionary([processed_data])

    bow_corpus = [dictionary.doc2bow(processed_data)]

    bow_doc_0 = bow_corpus[0]

    tfidf = models.TfidfModel(bow_corpus)

    corpus_tfidf = tfidf[bow_corpus]

    # LDA Model using Bag of Words
    lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=15, id2word=dictionary, passes=2, workers=4)

    topic_score_list = lda_model.show_topics(num_topics=1, num_words=15, log=False, formatted=False)[0][1]
    topics_list = [topic[0] for topic in topic_score_list]
    return(topics_list)



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
   article_df = pd.DataFrame(columns=['file','candidates','topics'])      # initialize dataframe for each article
   person_list = []
   person_names=person_list

   filepath = newspath + "/" + file
   data = open(filepath,'r',encoding='utf-8')

   new_data = data.read()
   get_names(new_data)
   article_df['file'] = pd.Series(dtype='str')
   article_df['file'] = file
   article_df['candidates'] = [person_names]
   topics = get_topics(new_data)
   article_df['topics'] = [topics]
   results_df = results_df.append(article_df)



results_df['file'] = results_df['file'].astype(str)
print(results_df)
exit()
