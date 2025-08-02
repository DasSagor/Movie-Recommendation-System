import streamlit as st
import pickle
import pandas as pd
import requests

movies_dash = pickle.load(open('movies.pkl','rb'))
movies_list = movies_dash['title'].values
similarity = pickle.load(open('similarity.pkl','rb'))


def recommend(movie):
    movie_index = movies_dash[movies_dash['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_movies = []
    for i in movies:
        recommend_movies.append(movies_dash.iloc[i[0]].title)
    return recommend_movies


st.title('Movie Recommender System')


selected_movie_name = st.selectbox(
    "Select a movie you like:",
    movies_list,
)


if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for i in recommendations:
        st.write(i)