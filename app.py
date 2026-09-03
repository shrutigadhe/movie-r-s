import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommender System", layout="wide", page_icon="🎬")

@st.cache_resource
def load_data_and_similarity():
    # Load movies dictionary (2.2 MB)
    with open('movies_dict.pkl', 'rb') as f:
        movies_dict = pickle.load(f)
    movies = pd.DataFrame(movies_dict)
    
    # Compute similarity matrix on startup (~1.4 seconds)
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()
    similarity = cosine_similarity(vectors)
    return movies, similarity

def fetch_poster(movie_id, api_key):
    if not api_key:
        return "https://via.placeholder.com/500x750?text=No+Poster"
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception:
        pass
    return "https://via.placeholder.com/500x750?text=No+Poster"

st.title("🎬 Movie Recommender System")
st.write("Discover movies similar to your favorites using content-based filtering.")

movies, similarity = load_data_and_similarity()

# Optional TMDB API key input in sidebar
st.sidebar.header("Configuration")
tmdb_api_key = st.sidebar.text_input("TMDB API Key (Optional for Posters)", type="password", help="Enter your TMDB API key to fetch real movie posters.")

selected_movie = st.selectbox(
    "Select or type a movie name:",
    movies['title'].values
)

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_names = []
    recommended_posters = []
    for i in movies_list:
        m_id = movies.iloc[i[0]].movie_id
        recommended_names.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(m_id, tmdb_api_key))
    return recommended_names, recommended_posters

if st.button("Recommend"):
    with st.spinner("Finding recommendations..."):
        names, posters = recommend(selected_movie)
    
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.caption(names[idx])
            st.image(posters[idx], use_container_width=True)
