import streamlit as st
st.title('Movie Recommender System')
option =st.selectbox(
    'how would you like to be contacted?',
    ('Email','Home Phone','Mobile Phone')
)