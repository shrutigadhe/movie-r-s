import streamlit as st
import pickle
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# Configure session with retries and a standard User-Agent header
# This prevents TMDb from dropping connection (WinError 10054 / ConnectionResetError)
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
})

def fetch_poster(movie_id):
    api_key = st.secrets["TMDB_API_KEY"]

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data.get("poster_path"):
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

        return "https://via.placeholder.com/500x750?text=No+Poster+Available"

    except Exception:
        return "https://via.placeholder.com/500x750?text=Poster+Unavailable"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


# Load data files

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
print("Your columns:", movies.columns.tolist())
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit App UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Updated to modern Streamlit columns layout
    cols = st.columns(5)
    for idx in range(5):
        with cols[idx]:
            st.text(names[idx])
            st.image(posters[idx])


