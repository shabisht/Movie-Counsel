# =========================== Imporitng required libraries ==============================================================================================
import streamlit as st
import pandas as pd
import pickle
# import joblib
from urllib.request import urlopen
from movie_counsel import *
# =========================== Fetching dataset and ML Model ==============================================================================================
    # using st.cache_resource will run globally for the first time only. for all the sessions later results will fetched from cache.

@st.cache_resource
def import_dataset_similarity_matrix():
    ''' This function will fetch and return pandas, numpy object for dataset and the ML Model respectively.
        Note:- Make sure this function is using streamlit's cache properties to avoid loading datasets on every refresh '''
    
    movies_df = pd.read_csv("dataset/complete_dataset_with_urls.csv", keep_default_na=False) # loading movies dataset
    
    # g_drive_url_joblib = "https://drive.google.com/uc?id=1-MxoPHx492LCSG45buqWYxycByHevZfe&confirm=t&uuid=742b2095-e0c5-4f0a-9f0e-8c9e1e0a5f5b&at=AB6BwCCo0Cg2rZlZuHXZhaAkms7S:1694004179033"
    g_drive_url_pkl = "https://drive.google.com/uc?id=1u7NLuxrBQKaN4Fj0KS2tt98Whz927BL-&confirm=t&uuid=2525fb6b-f249-4851-8036-27d3de86dad4&at=AB6BwCA59t4_ReTmngovNU0n1vNT:1694003393913"
    similarity = pickle.load(urlopen(g_drive_url_pkl)) # loading similarity matrix for Recommendation
    
    return movies_df, similarity
# ================================ Calling class movie_counsel ot build web app ====================================================================================

if __name__ == '__main__':
  
    movie_counsel_obj = movie_counsel() # creating object
    movies_df, similarity = import_dataset_similarity_matrix() # importing datasets, ML Model
    movie_counsel_obj.set_logo()
    movie_counsel_obj.set_title("Your Movie counseller")
    movie_counsel_obj.create_inputBar_selectBar_resetButton(movies_df)

    if(len(st.session_state.default)>0):
        movie_counsel_obj.set_title("Selected Movies")
        movie_counsel_obj.fetch_movie_details(movies_df, index_provided=False) # get all movie deatails for user's selected movies
        movie_counsel_obj.create_movie_grid(5) # show user's selected movies's cover in 5*5 grid
        movie_counsel_obj.set_title("Recommendations")
        movie_counsel_obj.recommend(similarity, n=5)
        movie_counsel_obj.fetch_movie_details(movies_df, index_provided=True) # get all movie deatails for recommended movies
        movie_counsel_obj.display_recommended_movie_details()