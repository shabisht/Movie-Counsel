# =========================== Imporitng required libraries ==============================================================================================
import streamlit as st
# ================================ Implementing OOPs to build WebApp ====================================================================================
class movie_counsel:

    def __init__(self):
        ''' This method will set the page configs and create the session variables for the app '''

        st.set_page_config(page_title='Movie Counsel',  layout='wide', page_icon=':clapper:')
        if "options" not in st.session_state:
            # st.write("session var creating")
            st.session_state['options'] = set()
            st.session_state['default'] = set()
            st.session_state['default_value'] = None
            st.session_state['input_value'] = ""
            st.session_state.recommended_movies_index = None
            st.session_state.movie_details_selected = None
            st.session_state.movie_details_recommended = None
            st.session_state.recom_movie_details = None
            st.session_state.toogleButton = False
            st.session_state.cntry_default = None
            st.session_state.cntry_list = set()
            st.session_state.genre_default = None
            st.session_state.genre_list = set()
            st.session_state.language_default = None
            st.session_state.language_list = set()
            st.session_state.kind_default = None
            st.session_state.kind_list = set()
            st.session_state.result_list = set()
            st.session_state.result_default = None
            st.session_state.apply_button = False
            st.session_state.disabled_selectBar = False
            st.session_state.disabled_inputBar = False
            st.session_state.slider_range = list(range(5,20))
            
    def set_source_data(self, movies_df, similarity):
         if "movies_df" not in st.session_state:
            st.session_state.movies_df = movies_df
            st.session_state.similarity = similarity
            st.session_state.filter_df = movies_df

    def set_logo(self):
        ''' This methods will set the WebApp logo '''
        cols = self.create_n_columns(5)
        cols[2].image("images/logo7.gif", use_column_width=True)
    
    def set_title(self, title_name):
        ''' This method will create st.title. It accepts a string to be diplayed as the Title'''
        st.title(title_name)

    def create_n_columns(self, n):
        ''' This method will create st.columns. we can pass the agruments to this method whatever we pass in st.columns like n=3 or n=[1,3,1]'''
        return [x for x in st.columns(n)]
  
    def todo_on_text_input_change(self):
        ''' This method will be invoked whenever the value of text_input label changes.
            On change the current value of multiselect label is stored in session_state variable so that while searching for next movie when the pages refreshes the current selected values do not get lost. '''

        # st.write("todocalled")
        st.session_state.input_value = st.session_state.InputMovieName
        if len(st.session_state.SearchedMovies)>0:
            st.session_state.default.update(st.session_state.SearchedMovies)
            st.session_state['default_value'] = st.session_state['default']

    def create_textInput(self):
        ''' This method creates the text_input label. It takes User's input for serching movies/series'''
        self.input_movie = st.text_input('', value=st.session_state['input_value'], key='InputMovieName', placeholder='Enter Movie/Series Name', label_visibility='collapsed', on_change = self.todo_on_text_input_change, disabled=st.session_state.disabled_inputBar)
        if self.input_movie != "":
            self.input_movie = self.input_movie.lower()
            index_list = st.session_state.movies_df[st.session_state.movies_df.name.str.contains(self.input_movie)].index.tolist()
            for x in index_list:
                st.session_state['options'].add(st.session_state.movies_df.name.iloc[x])
   
    def create_selectbar(self):
        ''' This method creates the multiselect label. User's selection can be seen here'''
        self.selectbar = st.multiselect("", key="SearchedMovies", options=sorted(list(st.session_state['options'])), default=st.session_state['default_value'], max_selections=5,label_visibility='collapsed', disabled=st.session_state.disabled_selectBar)
        if len(self.selectbar)>0:
            st.session_state.default.update(st.session_state.SearchedMovies)

    def todo_on_resetButton_clicked(self):
        if st.session_state.reset_button:
            st.session_state['options'] = set()
            st.session_state['default'] = set()
            st.session_state['default_value'] = None
            st.session_state['input_value'] = ""
            st.session_state.recommended_movies_index = None
            st.session_state.movie_details_selected = None
            st.session_state.movie_details_recommended = None
            st.session_state.recom_movie_details = None
            st.session_state.filter_df = st.session_state.movies_df
            st.session_state.cntry_default = None
            st.session_state.cntry_list = set()
            st.session_state.genre_default = None
            st.session_state.genre_list = set()
            st.session_state.language_default = None
            st.session_state.language_list = set()
            st.session_state.kind_default = None
            st.session_state.kind_list = set()
            st.session_state.result_list = set()
            st.session_state.result_default = None
            st.session_state.apply_button = False
            st.session_state.disabled_selectBar = False
            st.session_state.disabled_inputBar = False
            st.session_state.slider_range = list(range(5,20))

    def create_resetButton(self):
        ''' This method creates a Reset Button. It will reset all the session_state variables'''
        self.reset_button = st.button("Reset", key="reset_button", type='primary', on_click=self.todo_on_resetButton_clicked, use_container_width=True)
    
    def todo_on_toogle_change(self):
        if st.session_state.toogleButton:
            st.session_state.disabled_selectBar = True
            st.session_state.disabled_inputBar = True
            # st.session_state.default = set()
            # st.session_state.default_value = None

        else:
            st.session_state.disabled = False
            st.session_state.disabled_selectBar = False
            st.session_state.disabled_inputBar = False

    def create_toogle(self):
        self.toogle_button = st.toggle(":red[&#9776;]", key="toogleButton", help="Filter Movies" ,on_change=self.todo_on_toogle_change)

    def todo_on_country_change(self):
        if len(st.session_state.filterCountry)>0:
            st.session_state.cntry_list.update(st.session_state.filterCountry)
            st.session_state.cntry_default = st.session_state.cntry_list
    
    def todo_on_genre_change(self):
        if len(st.session_state.filterGenre)>0:
            st.session_state.genre_list.update(st.session_state.filterGenre)
            st.session_state.genre_default = st.session_state.genre_list

    def todo_on_kind_change(self):
        if len(st.session_state.filterKind)>0:
            st.session_state.kind_list.update(st.session_state.filterKind)
            st.session_state.kind_default = st.session_state.kind_list

    def todo_on_language_change(self):
        if len(st.session_state.filterLanguage)>0:
            st.session_state.language_list.update(st.session_state.filterLanguage)
            st.session_state.language_default = st.session_state.language_list

    def todo_on_resultList_change(self):
        if len(st.session_state.resultList)>0:
            st.session_state.result_list.update(st.session_state.resultList)
            st.session_state.result_default = st.session_state.result_list
            st.session_state.options.update(st.session_state.result_list)
            st.session_state.default.update(st.session_state.result_list)

        if len(st.session_state.default)>=2:
            st.session_state.slider_range = list(range(2,20))
        else:
            st.session_state.slider_range = list(range(5,20))

    def todo_on_applyButton_click(self):
        st.session_state.apply_button = st.session_state.applyButton

    def show_filters(self, np):
        if st.session_state.toogleButton:
            with st.expander("", expanded=True):
                st.subheader("Advanced Movie Search")
                st.select_slider("Recommendation per select Movie", key='recommendationSlider',value=5, options = st.session_state.slider_range)
                col1, col2 = st.columns(2)
                col3, col4 = st.columns(2)
                cntrySet = set()
                for x in st.session_state.movies_df.country.unique().tolist():
                    cntrySet.update(x.split(','))
                selected_cntry_list = col1.multiselect("Country", key="filterCountry", options=sorted(list(cntrySet)), default= st.session_state.cntry_default, on_change=self.todo_on_country_change)
               
                genreSet = set()
                for x in st.session_state.movies_df.genre.unique().tolist():
                    genreSet.update(x.split(','))
                selected_genre_list = col2.multiselect("Genre", key="filterGenre", options=sorted(list(genreSet)), default= st.session_state.genre_default, on_change=self.todo_on_genre_change)  
                selected_kind_list = col3.multiselect("Kind", key="filterKind", options=np.sort(st.session_state.movies_df.kind.unique()), default= st.session_state.kind_default, on_change=self.todo_on_kind_change)
                selected_language_list = col4.multiselect("Language", key="filterLanguage", options=np.sort(st.session_state.movies_df.languages.unique()), default= st.session_state.language_default, on_change=self.todo_on_language_change)
                # st.write(selected_cntry_list)
                if len(selected_cntry_list)!=0 or len(selected_genre_list)!=0 or len(selected_kind_list)!=0 or len(selected_language_list)!=0:
                    apply_button = st.button("Apply", key="applyButton", type='primary', on_click=self.todo_on_applyButton_click)
                    if st.session_state.apply_button:
                        if len(selected_cntry_list)!=0:
                            st.session_state.filter_df = st.session_state.movies_df[st.session_state.movies_df.country.str.contains('|'.join(selected_cntry_list))]
                        if len(selected_genre_list)!=0:
                            st.session_state.filter_df = st.session_state.filter_df[st.session_state.filter_df.genre.str.contains('|'.join(selected_genre_list))]
                        if len(selected_kind_list)!=0:
                            st.session_state.filter_df = st.session_state.filter_df[st.session_state.filter_df.kind.str.contains('|'.join(selected_kind_list))]
                        if len(selected_language_list)!=0:
                            st.session_state.filter_df = st.session_state.filter_df[st.session_state.filter_df.languages.str.contains('|'.join(selected_language_list))]
    
                        st.multiselect("",options=st.session_state.filter_df.name, key="resultList", default=st.session_state.result_default, max_selections=5, on_change=self.todo_on_resultList_change)
    
    def fetch_movie_details(self, index_provided = False):
        ''' If input value index_provided = False(default) then this method will fetch user's selected movies from movies dataset based on movie names and store it in a list of dictionaries. Each dictionary contains details of one movie.
            If index_provided = True, then this method will fetch details of recommended movies from movies dataset based on indexes provided by the recommend method and store it in a list of dictionaries. Each dictionary contains details of one movie.
              '''
        if not index_provided:
            st.session_state.movie_details_selected = []
            for movie in st.session_state.default:
                    index = st.session_state.movies_df[st.session_state.movies_df.name == movie].index[0]
                    temp = []
                    for i in range(st.session_state.movies_df.columns.shape[0]):
                        temp.append(st.session_state.movies_df.iloc[index, i])
                    temp.append(index)
                    col_names = st.session_state.movies_df.columns.tolist()
                    col_names.append('index')
                    st.session_state.movie_details_selected.append(dict(zip(col_names, temp)))
        else:
            st.session_state.movie_details_recommended = []
            for index in st.session_state.recommended_movies_index:
                temp = []
                for i in range(st.session_state.movies_df.columns.shape[0]):
                    temp.append(st.session_state.movies_df.iloc[index, i])
                col_names = st.session_state.movies_df.columns.tolist()
                st.session_state.movie_details_recommended.append(dict(zip(col_names, temp)))
    
    def create_movie_grid(self, n=5):
        ''' This method will create a 5*5 grid of user's selected movies. 
            Input n = number of movies to display as grid '''
        
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
        ''' This method will create a div container to show recommended movie details like plot, cast, genre, runtime etc.
            It creates a outer Container haivng 4 containers inside to display cover image, plot, movie info and casts '''

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
                         <p>Year - {movie['year']}</p>
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
                        <a href="https://www.imdb.com/title/{movie['id']}" target="_blank"><p>Visit IMDB</p></a>
                    </div>
                </div>
        """
        st.markdown(containers, unsafe_allow_html=True)

    def create_inputBar_selectBar_resetButton(self):
        ''' This method will call methods to create text_input label, multiselect label and reset button, align them with in a single row using st.columns'''
        
        cols = self.create_n_columns([2,6,1,1])
        with cols[0]:
            self.create_textInput()
        with cols[1]:
            self.create_selectbar()
        with cols[2]:
            self.create_toogle()
        with cols[3]:
            self.create_resetButton()

    def recommend(self):
        ''' this method will recommend movies based on user's selected movies using the st.session_state.similarity matrix.
            it will provide the indexes of the recommended movies '''
        n = 5
        if 'recommendationSlider' in st.session_state:
            n = st.session_state.recommendationSlider

        index_list = [x['index'] for x in st.session_state.movie_details_selected]
        st.session_state.recommended_movies_index = []
        for x in index_list:
            count = 0
            distances = st.session_state.similarity[x]
            movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:n*4]
            # print(movie_list);print(movie_list[0]);print(movie_list[0][0]);break
            for i in range(len(movie_list)):
                # print(movie_list[i][0])
                if movie_list[i][0] not in index_list and movie_list[i][0] not in st.session_state.recommended_movies_index:
                    st.session_state.recommended_movies_index.append(movie_list[i][0])
                    count+=1
                # print(i, count)
                if count == n:
                    break
        # st.session_state.recommended_movies_index = list(set(st.session_state.recommended_movies_index))

    def display_recommended_movie_details(self):
        ''' this method will show the the recommended movies with complete details inside a st.expander.
            It uses @create_custom_div_containers method to create div container '''

        with st.expander("See Complete Movie Details", expanded=True):
            for movie in st.session_state.movie_details_recommended:
                with st.container():
                    st.markdown(f'''<center><h2 style="color:#79cdff;font-style:rubik;font-weight:bold;">{movie['name'].title()}</h2></center>''', unsafe_allow_html=True)
                    self.create_custom_div_containers(movie)
                st.divider()