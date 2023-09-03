import pandas as  pd
import streamlit as st
import joblib
from traitlets import default
from PIL import Image

st.set_page_config(page_title='Movie Counsel',  layout='wide', page_icon=':clapper:')
st.title("Your Movie Counsel App")

@st.cache_resource
def import_dataset_similarity_matrix():
    movies_df = pd.read_csv("new_dataset.csv")
    similarity = joblib.load('similarity_8k.joblib')
    options = set()
    default = set()
    default_value = None
    return movies_df, similarity, options, default, default_value

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

movies_df, similarity, option_list, default_list, default_value = import_dataset_similarity_matrix()

def create_movie_grid(movie_details, n=5):
    urls = [f"{x['cover_url'].split('_V1_')[0]}.jpg" for x in movie_details]
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

def create_box(x):

    box_css = f"""
        <style>
            /* Define CSS variables for colors */
            :root {{
                --background-color: #36454F; /* Lighter shade of blue-gray background color */
                --text-color: #fff; /* Whitish text color */
                --border-color: #000; /* Black border color */
            }}

            /* CSS for the rectangular box */
            .box {{
                width: 100%; /* Make the box width adaptive to its parent */
                background-color: var(--background-color); /* Use the CSS variable for background color */
                border: 2px solid var(--border-color); /* Use the CSS variable for border color */
                padding: 1px;
                text-align: center;
                border-radius: 15px; /* Increased border-radius for rounder corners */
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2); /* Subtle box shadow */
            }}

            /* CSS for the text inside the box */
            .box p {{
                color: var(--text-color); /* Use the CSS variable for text color */
                font-size: 18px;
                font-style:lato;
            }}
        </style>
        <div class="box"><p>{x}</p></div>
    """
    st.markdown(box_css, unsafe_allow_html=True)

# st.write(option_list)
# st.write(default_list)

input_movie = st.text_input('', value="Avengers", key='InputMovieName', placeholder='Enter a Movie Name and get :cool: Recommendation')

if input_movie != "":
    input_movie = input_movie.lower()
    index_list = movies_df[movies_df.name.str.contains(input_movie)].index.tolist()
    for x in index_list:
        option_list.add(movies_df.name.iloc[x])

if len(default_list) != 0:
    default_value = list(default_list)
temp = st.multiselect("", key="SearchedMovies", options=sorted(list(option_list)), default=default_value, max_selections=10)
if len(temp) != 0:
    default_list.update(temp)

# print(temp)
# print(default_list)

# https://m.media-amazon.com/images/M/MV5BY2RiM2FkNjEtNzZhMS00MmY4LWIyMjUtNWExMzIyNDQ2YjY4XkEyXkFqcGdeQXVyMTM1MTE1NDMx._V1_SY150_CR0,0,101,150_.jpg
# https://m.media-amazon.com/images/M/MV5BZjhjMWE5OTUtOWNlMi00ZjM0LWE0YTktMWZkNmIwZmZkYzBjXkEyXkFqcGdeQXVyMjUzOTY1NTc@._V1_SX101_CR0,0,101,150_.jpg
# https://imdb-video.media-imdb.com/vi144884505/1434659607842-pgv4ql-1632113142638.mp4?Expires=1693813755&Signature=HljJycCo2QYh7pDWBFwkBDcGqFpqUKRykwABwg2SwzM92ZZ4LRBM0JYByAIBpo9lQBgXCRgO2S4hvSp-te-uz6ofsvXmcaUltrL4Fr41Fu0rxPCRv6SVfxfc6pP3l~jEyFov~BxMz5BodG~2gd956y4Az8UF3CW8zMsZFS4T1biWZzGqQtEofYPKeL7gYHUntyCGYwK6sS-P5xmvmUsv38XP13Qd0Uzcdq8SPT9BNy8-apQR4p0ET-uHCU7F6UpyAoMLT9FnHCTxuG6dyUzks-K-bbLLFcO16lSZspq6zXiUZqFebDJebt6IwgQ~wq2dR732zBNa~eFIXIebVyrhAg__&Key-Pair-Id=APKAIFLZBVQZ24NQH3KA

cols = [x for x in st.columns(6)]
recom_button = cols[0].button("Show Recommendation", type='primary')
reset_button = cols[1].button("Reset", type='primary')
if(len(default_list)>0):
    if recom_button:
        st.title("Selected Movies")
        movie_details = fetch_movie_details(default_list)
        create_movie_grid(movie_details, 5)
       
        st.title("Recommended Movies")
        index_list = [x['index'] for x in movie_details]
        recommended_movies_index = recommend(index_list, 5)
        recommended_movies_index = list(set(recommended_movies_index))
        # print(recommended_movies_index)
        recom_movie_details = fetch_movie_details(recommended_movies_index, index_provided=True)
        create_movie_grid(recom_movie_details,5)


        # clicked = clickable_images(urls,
        #     titles=[f"Image #{str(i)}" for i in range(5)],
        #     div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
        #     img_style={"margin": "5px", "height": "200px"},
        # )


        # with st.expander(f"movie {clicked} Details"):
        #     st.metric(movies_df.genre.iloc[0], value = movies_df.kind.iloc[0], delta=movies_df.rating.iloc[0])
        
        with st.expander("See Complete Movie Details", expanded=False):
            for movie in recom_movie_details:
                    with st.container():
                        col_exp1, col_exp2 = st.columns([1,4])
                        with col_exp1:
                            st.image(f"{movie['cover_url'].split('_V1_')[0]}.jpg")
                        with col_exp2:
                            create_box(movie['description'])
                            

    if reset_button:
        option_list.clear()
        default_list.clear()