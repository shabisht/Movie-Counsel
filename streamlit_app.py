# =========================== Imporitng required libraries ==============================================================================================
import streamlit as st
import pandas as pd
import joblib
from movie_counsel import *
# =========================== Fetching dataset and ML Model ==============================================================================================
    # using st.cache_resource will run globally for the first time only. for all the sessions later results will fetched from cache.

@st.cache_resource
def import_dataset_similarity_matrix():
    ''' This function will fetch and return pandas, numpy object for dataset and the ML Model respectively.
        Note:- Make sure this function is using streamlit's cache properties to avoid loading datasets on every refresh '''
    
    movies_df = pd.read_csv("dataset/complete_dataset_with_urls.csv", keep_default_na=False) # loading movies dataset
    similarity = joblib.load('dataset/similarity_8k.joblib') # loading similarity matrix for Recommendation
    return movies_df, similarity
# ================================ Calling class movie_counsel ot build web app ====================================================================================

if __name__ == '__main__':
  
    movie_counsel_obj = movie_counsel()
    movies_df, similarity = import_dataset_similarity_matrix()
    movie_counsel_obj.set_logo()
    movie_counsel_obj.set_title("Your Movie counseller")
    movie_counsel_obj.create_inputBar_selectBar_resetButton(movies_df)

    if(len(st.session_state.default)>0):
        movie_counsel_obj.set_title("Selected Movies")
        movie_counsel_obj.fetch_movie_details(movies_df, index_provided=False)
        movie_counsel_obj.create_movie_grid(5)
        movie_counsel_obj.set_title("Recommendations")
        movie_counsel_obj.recommend(similarity, n=5)
        movie_counsel_obj.fetch_movie_details(movies_df, index_provided=True)
        movie_counsel_obj.display_recommended_movie_details()