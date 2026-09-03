import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommender System", layout="wide", page_icon="🎬")

DEFAULT_API_KEY = "8265a5612470a7db5204423851b22e11"

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
    key_to_use = api_key.strip() if api_key and api_key.strip() else DEFAULT_API_KEY
    fallback_url = "https://placehold.co/500x750/1e293b/ffffff.png?text=Poster+Unavailable"
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={key_to_use}&language=en-US"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=4)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500" + poster_path
    except Exception:
        pass
    return fallback_url

st.title("🎬 Movie Recommender System")
st.write("Discover movies similar to your favorites using content-based filtering.")

movies, similarity = load_data_and_similarity()

# Sidebar configuration
st.sidebar.header("Configuration")
user_api_key = st.sidebar.text_input("Custom TMDB API Key (Optional)", type="password", help="Default working API key is active. Override with your own key if desired.")

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
        recommended_posters.append(fetch_poster(m_id, user_api_key))
    return recommended_names, recommended_posters

if st.button("Recommend"):
    with st.spinner("Fetching recommendations & movie posters..."):
        names, posters = recommend(selected_movie)
    
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.caption(names[idx])
            st.image(posters[idx], use_container_width=True)
