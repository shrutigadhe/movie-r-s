import streamlit as st
import pickle
import pandas as pd
import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Movie Recommender System", layout="wide", page_icon="🎬")

BACKUP_KEYS = [
    "888a7e0821d3f972b94f61f7db1387d8",
    "3fd2be6f0c70a2a598f084dd23fae7c6",
    "f809986b24cb4d2ed8839446d6b5e022",
    "6b7f3d5a1b3294b0d0c3453a2530bc4a"
]

@st.cache_resource
def load_data_and_similarity():
    with open('movies_dict.pkl', 'rb') as f:
        movies_dict = pickle.load(f)
    movies = pd.DataFrame(movies_dict)
    
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()
    similarity = cosine_similarity(vectors)
    return movies, similarity

def fetch_poster(movie_id, title, user_api_key):
    keys_to_try = []
    if user_api_key and user_api_key.strip():
        keys_to_try.append(user_api_key.strip())
    
    try:
        secret_key = st.secrets.get("TMDB_API_KEY", "")
        if secret_key:
            keys_to_try.append(secret_key)
    except Exception:
        pass
        
    keys_to_try.extend(BACKUP_KEYS)
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for key in keys_to_try:
        try:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=en-US"
            response = requests.get(url, headers=headers, timeout=3)
            if response.status_code == 200:
                data = response.json()
                poster_path = data.get('poster_path')
                if poster_path:
                    return f"https://image.tmdb.org/t/p/w500{poster_path}"
        except Exception:
            continue
            
    # Clean poster placeholder with movie title if API call fails
    encoded_title = requests.utils.quote(title)
    return f"https://placehold.co/500x750/1e293b/ffffff.png?text={encoded_title}"

st.title("🎬 Movie Recommender System")
st.write("Discover movies similar to your favorites using content-based filtering.")

movies, similarity = load_data_and_similarity()

st.sidebar.header("⚙️ Configuration")
user_key = st.sidebar.text_input("TMDB API Key (Optional)", type="password", help="Enter your personal TMDB API key to ensure 100% poster loading rate.")
st.sidebar.markdown("""
---
📌 **How to get your free TMDB API Key:**
1. Sign up at [themoviedb.org](https://www.themoviedb.org/signup)
2. Go to **Settings -> API**
3. Create a free API key & paste it above or add to Streamlit Secrets!
""")

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
        m_title = movies.iloc[i[0]].title
        recommended_names.append(m_title)
        recommended_posters.append(fetch_poster(m_id, m_title, user_key))
    return recommended_names, recommended_posters

if st.button("Recommend"):
    with st.spinner("Finding recommendations..."):
        names, posters = recommend(selected_movie)
    
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.caption(names[idx])
            st.image(posters[idx], use_container_width=True)
