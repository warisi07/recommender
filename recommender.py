# Importing necessary libraries
import pandas as pd
import numpy as np
import nltk    
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from nltk.tokenize import word_tokenize
import requests

# Load dataset, model and vectors
import pickle

df =  requests.get('https://firebasestorage.googleapis.com/v0/b/cornell-pickup.appspot.com/o/catalog.pkl?alt=media&token=dd5f5a72-52fc-4280-8f0e-7bf02aef3edc')
df = df.text

tfidf_vectors = requests.get('https://firebasestorage.googleapis.com/v0/b/cornell-pickup.appspot.com/o/vectors.pkl?alt=media&token=b87c3f06-62f0-47ee-9253-7b064e73b23b')
tfidf_vectors = tfidf_vectors.text

model= requests.get('https://firebasestorage.googleapis.com/v0/b/cornell-pickup.appspot.com/o/model.pkl?alt=media&token=c7fc9ca0-391f-4b58-b156-87d7b08fde5b')
model = model.text


# with open('https://firebasestorage.googleapis.com/v0/b/cornell-pickup.appspot.com/o/catalog.pkl?alt=media&token=dd5f5a72-52fc-4280-8f0e-7bf02aef3edc', 'rb') as f:
#     print('Loading dataset...')
#     df = pickle.load(f)

# with open('https://firebasestorage.googleapis.com/v0/b/cornell-pickup.appspot.com/o/vectors.pkl?alt=media&token=b87c3f06-62f0-47ee-9253-7b064e73b23b', 'rb') as f:
#     print('Loading tfidf vectors...')
#     tfidf_vectors = pickle.load(f)  

# with open('https://firebasestorage.googleapis.com/v0/b/cornell-pickup.appspot.com/o/model.pkl?alt=media&token=c7fc9ca0-391f-4b58-b156-87d7b08fde5b', 'rb') as f:
#     print('Loading model...')
#     model = pickle.load(f)

df = pd.DataFrame(df, columns=['subject code', 'course number', 
                           'course title', 'course description'])


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


def recommend_from_title(title, top_n):

    print('Getting recommendations...')
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
    sim_scores = sim_scores[1:top_n+1]
    course_indices = [i[0] for i in sim_scores]
    recommend = courses.iloc[course_indices]
    return recommend