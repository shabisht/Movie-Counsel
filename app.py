import pandas as  pd
import streamlit as st
import joblib

st.set_page_config(page_title='Movie Counsel',  layout='wide', page_icon=':clapper:')
# st.markdown("""<center><img src="images/logo7.gif" /></center>""", unsafe_allow_html=True)
c1, c2,c3,c4,c5 = st.columns(5)
c1.empty()
c2.empty()
c3.image("images/logo7.gif", use_column_width=True)
c4.empty()
c5.empty()
st.title("Your Movie Counsel App")

if "options" not in st.session_state:
    st.write("session var creating")
    st.session_state['options'] = set()
    st.session_state['default'] = set()
    st.session_state['default_value'] = None
    st.session_state['input_value'] = ""

@st.cache_resource
def import_dataset_similarity_matrix():
    movies_df = pd.read_csv("dataset/complete_dataset_with_urls.csv", keep_default_na=False)
    similarity = joblib.load('dataset/similarity_8k.joblib')
    # options = set()
    # default = set()
    # default_value = None
    return movies_df, similarity #, options, default, default_value

def recommend(index_list, n):
    recommended_movies_index = []
    for x in index_list:
        distances = similarity[x]
        # distances = similarity(movie_index)
        movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:(n+1)]
        recommended_movies_index+= [x[0] for x in movie_list]
    return recommended_movies_index

def fetch_movie_details(default_list, index_provided = False):
    movie_details = []
    if not index_provided:
        for movie in default_list:
                index = movies_df[movies_df.name == movie].index[0]
                temp = []
                for i in range(movies_df.columns.shape[0]):
                    temp.append(movies_df.iloc[index, i])
                temp.append(index)
                col_names = movies_df.columns.tolist()
                col_names.append('index')
                movie_details.append(dict(zip(col_names, temp)))
    else:
        for index in default_list:
            temp = []
            for i in range(movies_df.columns.shape[0]):
                temp.append(movies_df.iloc[index, i])
            col_names = movies_df.columns.tolist()
            movie_details.append(dict(zip(col_names, temp)))
    
    return movie_details

movies_df, similarity = import_dataset_similarity_matrix()

def create_movie_grid(movie_details, n=5):
    urls = []
    for x in movie_details:
        if x['cover_url'].startswith("https://t3"):
            urls.append(x['cover_url'])
        else:
            urls.append(f"{x['cover_url'].split('_V1_')[0]}.jpg")
    rows = len(movie_details)//n
    if len(movie_details)%n != 0:
        rows+=1
    for i in range(0,rows):
        with st.container():
            columns = [x for x in st.columns(n)]
            for j in range(0,len(columns)):
                columns[j].image(urls[n*i+j])
                if(n*i+j == len(movie_details)-1):
                    break

def create_rectangles(movie):
    runtime = "N/A"
    if movie['duration'] != "N/A":
        runtime = f"{movie['duration'].replace('.0','')} min"

    url = f"{movie['cover_url'].split('_V1_')[0]}.jpg"
    if movie['cover_url'].startswith("https://t3"):
            url = movie['cover_url']

    rectangles = f"""
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
    st.markdown(rectangles, unsafe_allow_html=True)

def todo():
    st.write("todocalled")
    st.session_state.input_value = st.session_state.InputMovieName
    if len(st.session_state.SearchedMovies)>0:
        st.session_state.default.update(st.session_state.SearchedMovies)
        st.session_state['default_value'] = st.session_state['default']

c1,c2,c3 = st.columns([1,3,1])
input_movie = c1.text_input('', value=st.session_state['input_value'], key='InputMovieName', placeholder='Enter Movie/Series Name', label_visibility='collapsed', on_change=todo)
# # st.markdown(st_input_bar_top, unsafe_allow_html=True)
if input_movie != "":
    input_movie = input_movie.lower()
    index_list = movies_df[movies_df.name.str.contains(input_movie)].index.tolist()
    for x in index_list:
        st.session_state['options'].add(movies_df.name.iloc[x])

temp = c2.multiselect("", key="SearchedMovies", options=sorted(list(st.session_state['options'])), default=st.session_state['default_value'], max_selections=5,label_visibility='collapsed')
if len(temp)>0:
    st.session_state.default.update(st.session_state.SearchedMovies)

reset_button = c3.button("Reset", type='primary')

if(len(st.session_state.default)>0):
    st.title("Selected Movies")
    movie_details = fetch_movie_details(st.session_state.default)
    create_movie_grid(movie_details, 5)
    st.title("Recommended Movies")
    index_list = [x['index'] for x in movie_details]
    recommended_movies_index = recommend(index_list, 5)
    recommended_movies_index = list(set(recommended_movies_index))
    # print(recommended_movies_index)
    recom_movie_details = fetch_movie_details(recommended_movies_index, index_provided=True)
    # create_movie_grid(recom_movie_details,5)
    with st.expander("See Complete Movie Details", expanded=False):
        for movie in recom_movie_details:
            with st.container():
                st.markdown(f'''<center><h2 style="color:#79cdff;font-style:rubik;font-weight:bold;">{movie['name'].title()}</h2></center>''', unsafe_allow_html=True)
                # col_exp1, col_exp2 = st.columns([1,4])
                # with col_exp1:
                #     st.image(f"{movie['cover_url'].split('_V1_')[0]}.jpg")
                # with col_exp2:
                create_rectangles(movie)
                # create_box(movie['description'])
            st.divider()

if reset_button:
    st.session_state['options'] = set()
    st.session_state['default'] = set()
    st.session_state['default_value'] = None
    st.session_state['input_value'] = ""