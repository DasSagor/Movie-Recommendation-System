import streamlit as st
import pickle
import pandas as pd
import requests

movies_dash = pickle.load(open('movies.pkl','rb'))
movies_list = sorted(movies_dash['title'].values)
similarity = pickle.load(open('similarity.pkl','rb'))


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"


def recommend(movie):
    movie_index = movies_dash[movies_dash['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_movies_names = []
    recommend_movies_poster = []
    for i in movies:
        movie_id = movies_dash.iloc[i[0]].movie_id
        recommend_movies_poster.append(fetch_poster(movie_id))
        recommend_movies_names.append(movies_dash.iloc[i[0]].title)
    return recommend_movies_names,recommend_movies_poster



st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie you like:",
    movies_list,
)


if st.button('Show Recommendations'):
    with st.spinner('🔎 Fetching recommendations...'):
        recommend_movies_names, recommend_movies_poster = recommend(selected_movie_name)

        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommend_movies_names[i])
                st.image(recommend_movies_poster[i])