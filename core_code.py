import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import re
import string

class Recommender:
    def __init__(self):
        self.df = pd.read_csv('data.csv')
        self.df['Describe'] = self.df['Describe'].apply(self.text_cleaning)
        self.rating = pd.read_csv('ratings.csv')
        self.rating = self.rating[:511]

    def unique_dishes(self):
        return list(self.df['Name'].unique())

    def text_cleaning(self, text):
        text = "".join([char for char in text if char not in string.punctuation])
        return text

    def content(self):
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['Describe'])
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)
        self.indices = pd.Series(self.df.index, index=self.df['Name']).drop_duplicates()

    def get_recom_con1(self, title, x = 0):
        self.content()
        cosine_sim = self.cosine_sim

        idx = self.indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 5 most similar food
        sim_scores = sim_scores[1:6]

        food_indices = [i[0] for i in sim_scores]
        return self.df['Name'].iloc[food_indices]

    def create_soup(self, x):
        return x['C_Type'] + " " + x['Veg_Non'] + " " + x['Describe']

    def get_recom_con2(self, title):
        self.df['soup'] = self.df.apply(self.create_soup, axis=1)
        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform(self.df['soup'])
        cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
        self.df = self.df.reset_index()
        self.indices = pd.Series(self.df.index, index=self.df['Name'])

        #self.get_recom_con1(title, cosine_sim2)
        idx = self.indices[title]
        sim_scores = list(enumerate(cosine_sim2[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # Get the scores of the 5 most similar food
        sim_scores = sim_scores[1:6]
        food_indices = [i[0] for i in sim_scores]
        return self.df['Name'].iloc[food_indices]

    def get_recom_colab(self, title):
        rating_matrix = self.rating.pivot_table(index='Food_ID', columns='User_ID', values='Rating').fillna(0)
        csr_rating_matrix =  csr_matrix(rating_matrix.values)
        recommender = NearestNeighbors(metric='cosine')
        recommender.fit(csr_rating_matrix)

        user = self.df[self.df['Name'] == title]
        user_index = np.where(rating_matrix.index == int(user['Food_ID']))[0][0]
        user_ratings = rating_matrix.iloc[user_index]
        reshaped = user_ratings.values.reshape(1, -1)
        distances, indices = recommender.kneighbors(reshaped, n_neighbors=16)
        nearest_neighbors_indices = rating_matrix.iloc[indices[0]].index[1:]
        nearest_neighbors = pd.DataFrame({'Food_ID': nearest_neighbors_indices})
        result = pd.merge(nearest_neighbors, self.df, on='Food_ID', how='left')
        return result.head()

