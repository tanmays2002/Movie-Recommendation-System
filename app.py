import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    responce = requests.get('https://api.themoviedb.org/3/movie/{}'
                 '?api_key=2f5383216bb63b3d65120e634930e6c4&language=en-US'.format(movie_id))
    data = responce.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies_pkl[movies_pkl['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies_names = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies_pkl.iloc[i[0]].movie_id
        recommended_movies_names.append(movies_pkl.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies_names,recommended_movies_posters


movies_pkl = pickle.load(open('movies.pkl','rb'))
movies = movies_pkl['title'].values


similarity = pickle.load(open('similarity.pkl','rb'))


st.title('Movie Recommender System')

selected_movie_name = st.selectbox("select any movie from the list",
             movies)

if st.button('Recommend'):
    recommended_movies_names,recommended_movies_posters= recommend(selected_movie_name)


    col1 ,col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movies_names[0])
        st.image(recommended_movies_posters[0])

    with col2:
        st.text(recommended_movies_names[1])
        st.image(recommended_movies_posters[1])

    with col3:
        st.text(recommended_movies_names[2])
        st.image(recommended_movies_posters[2])

    with col4:
        st.text(recommended_movies_names[3])
        st.image(recommended_movies_posters[3])

    with col5:
        st.text(recommended_movies_names[4])
        st.image(recommended_movies_posters[4])