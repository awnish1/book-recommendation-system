import streamlit as st

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

books=pd.read_csv("Books.csv", encoding="latin-1",low_memory=False)
ratings=pd.read_csv("Ratings.csv")
users=pd.read_csv("Users.csv")

ratings_with_names=ratings.merge(books,on='ISBN')

avg_rating_df=ratings_with_names.groupby('Book-Title')['Book-Rating'].mean().reset_index()
avg_rating_df=avg_rating_df.rename(columns={'Book-Rating':'avg_rating'})

num_rating_df=ratings_with_names.groupby('Book-Title')['Book-Rating'].count().reset_index()
num_rating_df=num_rating_df.rename(columns={'Book-Rating':'Number-Of-Rater'})

avg_rating_df=ratings_with_names.groupby('Book-Title')['Book-Rating'].mean().reset_index()
avg_rating_df=avg_rating_df.rename(columns={'Book-Rating':'avg_rating'})

popular_df=num_rating_df.merge(avg_rating_df, on='Book-Title')
popular_df=popular_df[popular_df['Number-Of-Rater']>=250].sort_values('avg_rating',ascending=False).head()
popular_df = popular_df.drop_duplicates('Book-Title')

experienced_users=ratings_with_names.groupby('User-ID')['Book-Rating'].count()>200
experienced_users=experienced_users[experienced_users].index

filtered_ratings=ratings_with_names[ratings_with_names['User-ID'].isin(experienced_users)]

popular_books=filtered_ratings.groupby('Book-Title')['Book-Rating'].count()>=50
popular_books=popular_books[popular_books].index

final_ratings=filtered_ratings[filtered_ratings['Book-Title'].isin(popular_books)]

pt=final_ratings.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')

pt=pt.fillna(0)

similarity_score=cosine_similarity(pt)

def recommend(book_name):

    index=np.where(pt.index==book_name)[0][0]
    similar_books=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1],reverse=True)[1:6]

    data=[]

    for i in similar_books:
        book_title=pt.index[i[0]]

        temp_df=books[books['Book-Title']==book_title]

        book_image=temp_df['Image-URL-M'].values[0]

        data.append((book_title, book_image))

    return data

def get_books():
    return pt.index.values



