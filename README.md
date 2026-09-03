# 🎬 Movie Recommender System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-FF4B4B?logo=streamlit&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.8-F7931E?logo=scikit-learn&logoColor=white)
![TMDB API](https://img.shields.io/badge/TMDB%20API-v3-01b4e4?logo=themoviedb&logoColor=white)
![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit%20Cloud-brightgreen?logo=streamlit)

A content-based recommendation engine built over a dataset of **4,800+ movies** using text vectorization and cosine similarity. Integrated with an interactive **Streamlit** web application and the **TMDB API** for real-time poster retrieval.

🚀 **Live Web App:** [shrutigadhe-movie-r-s-app-amddvv.streamlit.app](https://shrutigadhe-movie-r-s-app-amddvv.streamlit.app)

---

## ✨ Features

- 🎯 **Content-Based Filtering:** Recommends the top 5 most similar movies based on plot overviews, genres, keywords, top cast members, and directors.
- 🖼️ **Real-Time Poster Fetching:** Integrated with TMDB (The Movie Database) API for live movie poster retrieval.
- 🔄 **Resilient Failover Architecture:** Implements multi-key API failover and dynamic fallback cards to ensure uninterrupted poster rendering.
- ⚡ **Sub-Second Inference:** Serialized processed movie metadata (`movies_dict.pkl`) and vectorized features enable recommendation lookup in **< 3 ms**.
- 🌐 **Interactive Streamlit Web UI:** Clean, responsive interface for seamless movie search and discovery.

---

## 📊 Key Project Benchmarks

- **Dataset Size:** `4,800+` movies (`tmdb_5000_movies.csv` and `tmdb_5000_credits.csv`).
- **Feature Engineering Runtime:** `~19 seconds` full end-to-end preprocessing pipeline.
- **Inference Speed:** `Sub-second (< 3 ms)` recommendation retrieval time.
- **Vocabulary Size:** `5,000` max features extracted via `CountVectorizer` and NLTK `PorterStemmer`.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **Data Manipulation & Analysis:** [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Machine Learning & NLP:** [Scikit-Learn](https://scikit-learn.org/) (`CountVectorizer`, `cosine_similarity`), [NLTK](https://www.nltk.org/) (`PorterStemmer`)
- **API Integration:** [Requests](https://requests.readthedocs.io/) & TMDB API v3
- **Model Serialization:** [Pickle](https://docs.python.org/3/library/pickle.html)

---

## 📐 Architecture & Workflow

```
[Raw Datasets] (movies.csv + credits.csv)
       │
       ▼
[Data Cleaning & Feature Engineering]
       ├── Extract Genres, Keywords, Cast & Crew (Director)
       ├── Clean whitespace & combine into unified 'tags'
       └── Text Normalization (NLTK PorterStemmer)
       │
       ▼
[Vectorization & Similarity Matrix]
       ├── CountVectorizer (5,000 top features)
       └── Cosine Similarity Matrix Computation
       │
       ▼
[Streamlit Deployment]
       ├── Cached similarity calculation (@st.cache_resource)
       ├── TMDB API Poster Fetching & Multi-Key Failover
       └── Interactive Web Display
```

---

## 🚀 Quick Start (Run Locally)

### 1. Clone the Repository
```bash
git clone https://github.com/shrutigadhe/movie-r-s.git
cd movie-r-s
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit App
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ Deploying on Streamlit Cloud

1. Push code to your GitHub repository.
2. Log in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click **"New App"** -> Select Repository `shrutigadhe/movie-r-s` -> Branch `main` -> Main file `app.py`.
4. Click **Deploy!**

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
