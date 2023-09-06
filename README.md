# Movie Counsel - Your own 🍿 Movie/Series Recommender-System.
[![Site](https://img.shields.io/static/v1?label=visit%20Website&message=Movie%20Counsel%20Page&color=yellow)](https://movie-counsel.streamlit.app)
[![Linkedin](https://img.shields.io/static/v1?label=visit&message=My%20Linkedin%20Page&color=blue&logo=linkedin)](https://www.linkedin.com/in/shailesh-bisht-b42a73184/)
[![Hosted-on](https://img.shields.io/static/v1?label=made%20with&message=Streamlit&color=c21a09&logo=streamlit)](https://streamlit.io/)
[![python](https://img.shields.io/static/v1?label=Python&message=%3E=3.9&color=brown&logo=python)]()
<br>

## 1. App Intro
This Streamlit based Web app helps you find the right recommendation for your favourite Movies or TV Shows. Find movies from differrent genres and get recommendation for the same.
* App Features
    - Content + Popularity Based
    - Based on  [IMDB Movies Dataset](https://www.kaggle.com/datasets/ashishjangra27/imdb-movies-dataset)
    - Search and select max 5 Movies of your choice and get recommendation for those movies, with complete details like Cover Photo, Plot, Genre, Runtime, Country, Language, Kind, Director, Star-Cast etc.

### i). What do I need to make it work?
Python 3.9 or later and must have below pypi packages
```
streamlit >= ver- 1.26.0
pandas
pickle
```
Or Simply run `pip install -r requirements.txt`

### ii). How does it work?
    * Web app is developed using Streamlit.
    * Pandas is used for Data Analysis.
    * Joblib is used for storing and loading the ML Mode.

## 2. Data Analysis
### i). Source Data
    * <b>Source</b> - [IMDB Movies Dataset](https://www.kaggle.com/datasets/ashishjangra27/imdb-movies-dataset) from Kaggle
    * <b>Description</b> - This dataset is having the data of 2.5 Million Movies/series listed on the official website of IMDB
    * <b>Features</b>
    - id - Movie ID
    - name - Name of the Movie
    - year - Year of movie release
    - rating - Rating of the Movie out of 10
    - certificate - Movie Certification
    - duration - Duration of the Movie in minutes
    - genre - Genre of the Movie
    - votes - Number of people who voted for the IMDB rating
    - gross_income - Gross Income of the Movie in Million
    - directors_id - ID of Directors who have worked on the movie

### ii). EDA
    * Data Pre-processing and Data Cleaning is done on around 2.5M data records.
    * Following Python Packages are used for analysis: -
        - EDA - Pandas, Numpy, re, scikit-learn, Cinemagoer
        - Data Visualization - plotly, seaborn, matplotlib
        - creating movie tags - nltk's Porter Stemmer
    * Please refer to the jupyter notebooks in this [📁](https://drive.google.com/drive/u/0/folders/1eYmIMKxbsw8CXg6qKJDU2NTP6qwkv0C9),these were used while Data Pre-processing and Data Cleaning.

### iii). Movie Recommender Model
    * Python Package <b>Cinemagoer</b> is used for fetching missing details from IMDB based on Movie's IMDB-ID for most of the records in the dataset.
    * movie tags are created for each movie by combining plot details, runtime details, year, genre, director, star-cast etc.
    * Nltk is used for stemming the words of movie tag. Stemming in NLP is basically the process of reducing a word to its word stem that affixes to suffixes and prefixes or the roots.
    * Scikit-learn's TfidifVectorizer (Term Frequency Inverse Document Frequency) is used to transform text into a meaningful representation of numbers which is used to fit machine algorithm for prediction. Basically it calculates how relevant a word in a series or corpus is to a text. The meaning increases proportionally to the number of times in the text a word appears but is compensated by the word frequency in the corpus (data-set).
    * Cosine_similarity matrix is used for finding the closet movies(documents) for a given movie (document). Basically it measures the similarity between two vectors or matrices based on their angle rather than distances like Euclidean or Manhattan etc.

## 3. Web App
    * Streamlit is used for building the web app.
    * ML Model i.e., the similarity matrix being bigger in size is stored in [G-Drive](https://drive.google.com/drive/u/0/folders/1eYmIMKxbsw8CXg6qKJDU2NTP6qwkv0C9)
    * Stremlit Cloud is used for hosting the web app.
## 4. Find the demo below
[![Demo]()]()