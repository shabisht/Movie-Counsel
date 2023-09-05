import streamlit as st
import pandas as pd
import joblib

@st.cache_resource
def import_dataset_similarity_matrix():
    movies_df = pd.read_csv("dataset/complete_dataset_with_urls.csv", keep_default_na=False)
    similarity = joblib.load('dataset/similarity_8k.joblib')
    return movies_df, similarity

class movie_counsel:
    def __init__(self):
        st.set_page_config(page_title='Movie Counsel',  layout='wide', page_icon=':clapper:')
        if "options" not in st.session_state:
            st.write("session var creating")
            st.session_state['options'] = set()
            st.session_state['default'] = set()
            st.session_state['default_value'] = None
            st.session_state['input_value'] = ""
            st.session_state.recommended_movies_index = None
            st.session_state.movie_details_selected = None
            st.session_state.movie_details_recommended = None
            st.session_state.recom_movie_details = None
  
    def set_logo(self):
        cols = self.create_n_columns(5)
        cols[2].image("images/logo7.gif", use_column_width=True)
    
    def set_title(self, title_name):
        st.title(title_name)

    def create_n_columns(self, n):
        return [x for x in st.columns(n)]
  
    def todo_on_text_input_change(self):
        st.write("todocalled")
        st.session_state.input_value = st.session_state.InputMovieName
        if len(st.session_state.SearchedMovies)>0:
            st.session_state.default.update(st.session_state.SearchedMovies)
            st.session_state['default_value'] = st.session_state['default']

    def create_textInput(self):
        self.input_movie = st.text_input('', value=st.session_state['input_value'], key='InputMovieName', placeholder='Enter Movie/Series Name', label_visibility='collapsed', on_change = self.todo_on_text_input_change)
        
    def create_selectbar(self):
        self.selectbar = st.multiselect("", key="SearchedMovies", options=sorted(list(st.session_state['options'])), default=st.session_state['default_value'], max_selections=5,label_visibility='collapsed')
        if len(self.selectbar)>0:
            st.session_state.default.update(st.session_state.SearchedMovies)
        
    def create_resetButton(self):
        self.reset_button = st.button("Reset", key="reset_button", type='primary')
    
    def fetch_movie_details(self, default_list, index_provided = False):
        if not index_provided:
            st.session_state.movie_details_selected = []
            for movie in st.session_state.default:
                    index = movies_df[movies_df.name == movie].index[0]
                    temp = []
                    for i in range(movies_df.columns.shape[0]):
                        temp.append(movies_df.iloc[index, i])
                    temp.append(index)
                    col_names = movies_df.columns.tolist()
                    col_names.append('index')
                    st.session_state.movie_details_selected.append(dict(zip(col_names, temp)))
        else:
            st.session_state.movie_details_recommended = []
            for index in st.session_state.recommended_movies_index:
                temp = []
                for i in range(movies_df.columns.shape[0]):
                    temp.append(movies_df.iloc[index, i])
                col_names = movies_df.columns.tolist()
                st.session_state.movie_details_recommended.append(dict(zip(col_names, temp)))
    
    def create_movie_grid(self, n=5):
        urls = []
        for x in st.session_state.movie_details_selected:
            if x['cover_url'].startswith("https://t3"):
                urls.append(x['cover_url'])
            else:
                urls.append(f"{x['cover_url'].split('_V1_')[0]}.jpg")
        rows = len(st.session_state.movie_details_selected)//n
        if len(st.session_state.movie_details_selected)%n != 0:
            rows+=1
        for i in range(0,rows):
            with st.container():
                columns = self.create_n_columns(n)
                for j in range(0,len(columns)):
                    columns[j].image(urls[n*i+j])
                    if(n*i+j == len(st.session_state.movie_details_selected)-1):
                        break
    
    def create_custom_div_containers(self, movie):
        runtime = "N/A"
        if movie['duration'] != "N/A":
            runtime = f"{movie['duration'].replace('.0','')} min"
        url = f"{movie['cover_url'].split('_V1_')[0]}.jpg"
        if movie['cover_url'].startswith("https://t3"):
                url = movie['cover_url']
        containers = f"""
                <style>
                    /* CSS for the outer container */
                    .outer-container {{
                        display: flex;
                        justify-content: space-evenly;
                        align-items: center;
                    }}

                    /* CSS for the individual rectangular boxes */

                    .rect_box_img {{
                        width: 300px;
                        height: 350px;
                        background-color: #262730;
                        border-radius: 10px;
                        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                        margin: 0px; /* Adjust the margin to control the spacing */
                    }}

                    .rect_box_img img {{
                        width: 100%; /* Adjust image width to 100% of parent (Box 1) */
                        height: 100%; /* Adjust image height to 100% of parent (Box 1) */
                        max-width: 100%; /* Ensure image doesn't exceed parent width */
                        max-height: 100%; /* Ensure image doesn't exceed parent height */
            
                    }}

                    .rect_box {{
                        width: 300px;
                        height: 350px;
                        background-color: #262730;
                        border-radius: 10px;
                        text-align: center;
                        padding: 3px;
                        color: #fff;
                        font-size: 12px;
                        font-weight: bold;
                        font-family:courier;
                        box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                        margin: 8px; /* Adjust the margin to control the spacing */
                        font-size: 5vw; /* Responsive font size based on viewport width (adjust as needed) */
                        overflow: scroll; /* Hide text overflow */
                        transition: transform 0.2s, box-shadow 0.2s, background-color 0.2s; /* Apply transition effects */
                    }}

                    .rect_box-text-container {{
                    height: 100%; /* Set a fixed height for the text container */
                    overflow-y: auto; /* Add vertical scroll when text overflows */
                }}
                /* CSS for the hover state */
                .rect_box:hover {{
                    transform: scale(1.1); /* Scale the box up on hover */
                    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.4); /* Add a stronger box shadow on hover */
                    background-color: #778899;  /*#2980b9;Change the background color on hover */
                    
                }}
                </style>
                <!-- Outer container for centering -->
                <div class="outer-container">
                    <!-- Rectangular Box 1 -->
                    <div class="rect_box_img">
                        <img src="{url}" alt="Image in Box 1">
                    </div>
                    <!-- Rectangular Box 2 -->
                    <div class="rect_box">
                        <center><h4 style="font-weight:bold;font-family:rubik;color:#FF3A4A;">Plot</h4></center>
                        <p>{movie['description']}</p>
                    </div>
                    <!-- Rectangular Box 3 -->
                    <div class="rect_box">
                        <center><h4 style="font-weight:bold;font-family:rubik;color:#FF3A4A;">Info</h4></center>
                        <p>Type - {movie['kind']}</p>
                        <p>Rating - {movie['rating']}🌟</p>
                        <p>Genre - {movie['genre']}</p>
                        <p>Runtime - {runtime}</p>
                        <p>Country - {movie['country']}</p>
                        <p>Language - {movie['languages']}</p>
                    </div>
                    <!-- Rectangular Box 4 -->
                    <div class="rect_box">
                        <center><h4 style="font-weight:bold;font-family:rubik;color:#FF3A4A;">Cast</h4></center>                    
                        <p>Star Cast - {movie['stars']}</p>
                        <p>Director - {movie['directors']}</p>
                    </div>
                </div>
        """
        st.markdown(containers, unsafe_allow_html=True)

    def set_selectBar_options_as_per_inputMovie(self):
        if self.input_movie != "":
            self.input_movie = self.input_movie.lower()
            index_list = movies_df[movies_df.name.str.contains(self.input_movie)].index.tolist()
            for x in index_list:
                st.session_state['options'].add(movies_df.name.iloc[x])

    def create_inputBar_selectBar_resetButton(self):
        cols = movie_counsel_obj.create_n_columns([1,3,1])
        with cols[0]:
            movie_counsel_obj.create_textInput()
            movie_counsel_obj.set_selectBar_options_as_per_inputMovie()
        with cols[1]:
            movie_counsel_obj.create_selectbar()
        with cols[2]:
            movie_counsel_obj.create_resetButton()

    def recommend(self, n=5):
        index_list = [x['index'] for x in st.session_state.movie_details_selected]
        st.session_state.recommended_movies_index = []
        for x in index_list:
            distances = similarity[x]
            # distances = similarity(movie_index)
            movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:(n+1)]
            st.session_state.recommended_movies_index+= [x[0] for x in movie_list]
        st.session_state.recommended_movies_index = list(set(st.session_state.recommended_movies_index))

    def display_recommended_movie_details(self):
        with st.expander("See Complete Movie Details", expanded=True):
            for movie in st.session_state.movie_details_recommended:
                with st.container():
                    st.markdown(f'''<center><h2 style="color:#79cdff;font-style:rubik;font-weight:bold;">{movie['name'].title()}</h2></center>''', unsafe_allow_html=True)
                    self.create_custom_div_containers(movie)
                st.divider()


if __name__ == '__main__':
    movie_counsel_obj = movie_counsel()
    movie_counsel_obj.set_logo()
    movie_counsel_obj.set_title("YOur Movie Couseller")
    movies_df, similarity = import_dataset_similarity_matrix()
    movie_counsel_obj.create_inputBar_selectBar_resetButton()
    if(len(st.session_state.default)>0):
        movie_counsel_obj.set_title("Selected Movies")
        movie_counsel_obj.fetch_movie_details(st.session_state.default)
        movie_counsel_obj.create_movie_grid(5)
        movie_counsel_obj.set_title("Recommendations")
        movie_counsel_obj.recommend(n=5)
        movie_counsel_obj.fetch_movie_details(st.session_state.recommended_movies_index, index_provided=True)
        movie_counsel_obj.display_recommended_movie_details()
    if st.session_state.reset_button:
        st.session_state['options'] = set()
        st.session_state['default'] = set()
        st.session_state['default_value'] = None
        st.session_state['input_value'] = ""
        st.session_state.recommended_movies_index = None
        st.session_state.movie_details_selected = None
        st.session_state.movie_details_recommended = None
        st.session_state.recom_movie_details = None