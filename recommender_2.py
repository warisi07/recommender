# -*- coding: utf-8 -*-
"""recommender.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_gs2d7cuclsLnJYULYXto0XBMvOwaWNj
"""

# Importing necessary libraries
print('Installing libraries...')
import pandas as pd
import numpy as np
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context =   _create_unverified_https_context  
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import Word2Vec
from matplotlib import pyplot
from gensim.models import KeyedVectors
import pandas as pd
from nltk.tokenize import word_tokenize



# Load dataset 
import pickle
with open('./catalog.pkl', 'rb') as f:
    df = pickle.load(f)

df = pd.DataFrame(df, 
                  columns=['subject code', 'course number', 
                           'course title', 'course description'])

# Pre-processing
def _removeNonAscii(s):
    return "".join(i for i in s if  ord(i)<128)

def make_lower_case(text):
    return text.lower()

def remove_stop_words(text):
    text = text.split()
    stops = set(stopwords.words("english"))
    text = [w for w in text if not w in stops]
    text = " ".join(text)
    return text

def remove_html(text):
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)

def remove_punctuation(text):
    tokenizer = RegexpTokenizer(r'\w+')
    text = tokenizer.tokenize(text)
    text = " ".join(text)
    return text

print('Pre-processing data...')
df['desc'] = df['course description'].apply(_removeNonAscii)
df['desc'] = df.desc.apply(func = make_lower_case)
df['desc'] = df.desc.apply(func = remove_stop_words)
df['desc'] = df.desc.apply(func=remove_punctuation)
df['desc'] = df.desc.apply(func=remove_html)



"""
## TF-IDF Word2Vec Model
"""

# Tokenize words
print('Tokenizing words...')
corpus = []
for words in df['desc']:
    corpus.append(word_tokenize(words))

#Building TFIDF model and calculate TFIDF score for descriptions
tfidf = TfidfVectorizer(analyzer='word', ngram_range=(1, 3), min_df = 5, stop_words='english')
tfidf.fit(df['desc'])


# Getting the words from the TF-IDF model
tfidf_list = dict(zip(tfidf.get_feature_names_out(), list(tfidf.idf_)))
tfidf_feature = tfidf.get_feature_names_out()

# Using google pretrained Word2vec model with over 2 billion words
import urllib.request
print('Loading pretrained model...')
pretrained_model=  urllib.request.urlopen('https://firebasestorage.googleapis.com/v0/b/recommender-2c699.appspot.com/o/pretrained.pkl?alt=media&token=d8506d5b-2a58-4373-8e77-bd046afa688a')

model = Word2Vec(vector_size=300, window=5, min_count=1, workers=4)
model.build_vocab(corpus)

model.build_vocab([list(pretrained_model.key_to_index.keys())], update=True)

print('Training model...')
model.train(corpus, total_examples=model.corpus_count, epochs=5)

# Averaging the vectors of each word to get sentence embeddings is not the best
# approach, so this is using the tfidf vectors to weight it.

print('Creating sentence embeddings...')
tfidf_vectors = []
line = 0;

for desc in corpus:
  sent_vec = np.zeros(300)
  weight_sum = 0
  for word in desc:
    if word in model.wv.key_to_index and word in tfidf_feature:
      vec = model.wv[word]
      tf_idf = tfidf_list[word] * (desc.count(word) / len(desc))
      sent_vec += (vec * tf_idf)
      weight_sum += tf_idf
  if weight_sum != 0:
        sent_vec /= weight_sum
  tfidf_vectors.append(sent_vec)
  line += 1

print('Done!')

def recommend_from_keyword(keywords, top_n):

    print('Getting recommendations...')
    
    keywords = [word_tokenize(keywords)]
    
    keyword_vectors = []


    for line in keywords:
        avgword2vec = None
        count = 0
        for word in line:
            if word in model.wv.key_to_index :
                count += 1
                if avgword2vec is None:
                    avgword2vec = model.wv[word]
                else:
                    avgword2vec = avgword2vec + model.wv[word]
                
        if avgword2vec is not None:
            avgword2vec = avgword2vec / count
        
            keyword_vectors.append(avgword2vec)
                    
    cosine_similarities = cosine_similarity(keyword_vectors, tfidf_vectors)
    avg_scores = cosine_similarities.mean(axis=0)
    top_recommendations = np.argsort(avg_scores)[::-1][:top_n]
    df_recommended = []
    for i in top_recommendations:
        df_recommended.append(df.iloc[i])
    return pd.DataFrame(df_recommended, columns=['subject code', 'course number', 
                           'course title'])


def recommend_from_title(title):
      cosine_similarities = cosine_similarity(tfidf_vectors,  tfidf_vectors)
      courses = df[['course title', 'subject code', 'course number']]
      indices = pd.Series(df.index, index = df['course title'])
        
      idx = indices[title]
      # Temporary fix : some courses titles are duplicated. 
      # Trying to keep the duplicates because they come from
      # different departments. 
      if isinstance(idx, pd.core.series.Series):
            idx = idx[0]
      sim_scores = list(enumerate(cosine_similarities[idx]))
      sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
      sim_scores = sim_scores[1:21]
      course_indices = [i[0] for i in sim_scores]
      recommend = courses.iloc[course_indices]
      return recommend

