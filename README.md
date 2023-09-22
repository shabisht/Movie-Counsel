# Movie Counsel - Your own 🍿 Movie/Series Recommender-System.
[![Site](https://img.shields.io/static/v1?label=visit%20Website&message=Movie%20Counsel%20Page&color=yellow)](https://movie-counsel.streamlit.app)
[![Linkedin](https://img.shields.io/static/v1?label=visit&message=My%20Linkedin%20Page&color=blue&logo=linkedin)](https://www.linkedin.com/in/shailesh-bisht-b42a73184/)
[![Hosted-on](https://img.shields.io/static/v1?label=made%20with&message=Streamlit&color=c21a09&logo=streamlit)](https://streamlit.io/)
[![python](https://img.shields.io/static/v1?label=Python&message=%3E=3.9&color=brown&logo=python)]()
<br>

# App Introduction
This Streamlit based Web app helps you find the right recommendation for your favourite Movies or TV Shows with an inbuilt Movie Review Sentiment Analyzer tool.

## 1. Movie Recommeder System
- App Features
    - Content + Popularity Based
    - Based on  [IMDB Movies Dataset](https://www.kaggle.com/datasets/ashishjangra27/imdb-movies-dataset)
    - Search and select max 5 Movies of your choice and get recommendation for those movies, with complete details like Cover Photo, Plot, Genre, Runtime, Country, Language, Kind, Director, Star-Cast etc.

### Data Analysis
#### i). Source Data
- <b>Source</b> - [IMDB Movies Dataset](https://www.kaggle.com/datasets/ashishjangra27/imdb-movies-dataset) from Kaggle
- <b>Description</b> - This dataset is having the data of 2.5 Million Movies/series listed on the official website of IMDB
- <b>Features</b>
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

#### ii). EDA
- Data Pre-processing and Data Cleaning is done on around 2.5M data records.
- Following Python Packages are used for analysis: -
    - **EDA** - Pandas, Numpy, re, scikit-learn
    - **Data Visualization** - plotly, seaborn, matplotlib
- Please refer to this **[notebook](https://colab.research.google.com/drive/1isHjN0l2HUsofaH0jIsHeZSBQ_2VHn6G)** for complete detailed analysis, also check out other files in this **[📁](https://drive.google.com/drive/u/0/folders/1eYmIMKxbsw8CXg6qKJDU2NTP6qwkv0C9)**,all these are part of the Data Pre-processing and Data Cleaning.

#### iii). Movie Recommender Model
- Python Package **Cinemagoer** is used for fetching missing details from IMDB based on Movie's IMDB-ID for most of the records in the dataset.
- movie tags are created for each movie by combining plot details, runtime details, year, genre, director, star-cast etc.
- **Nltk's Porter Stemmer** is used for **stemming** the words of movie tag. Stemming in NLP is basically the process of reducing a word to its word stem that affixes to suffixes and prefixes or the roots.
- Scikit-learn's **TfidifVectorizer** (Term Frequency Inverse Document Frequency) is used to transform text into a meaningful representation of numbers which is used to fit machine algorithm for prediction. Basically it calculates how relevant a word in a series or corpus is to a text. The meaning increases proportionally to the number of times in the text a word appears but is compensated by the word frequency in the corpus (data-set).
- Scikit-learn's **Cosine_Similarity** matrix is used for finding the closet movies(documents) for a given movie (document). Basically it measures the similarity between two vectors or matrices based on their angle rather than distances like Euclidean or Manhattan etc.
- Please refer to this **[notebook](https://colab.research.google.com/drive/1DKl9RipdzavlXmgZ73fxI9lEfBzpJmGk)** for complete detailed analysis, also check out other files in this **[📁](https://drive.google.com/drive/u/0/folders/1eYmIMKxbsw8CXg6qKJDU2NTP6qwkv0C9)**,all these are part of the Data Pre-processing and Data Cleaning.


## 2. Sentiment Analyzer

[Sentiment Analyzer](https://movie-counsel.streamlit.app/Sentiment_Analysis) for Movie Reviews is a comprehensive tool designed to evaluate the sentiment of movie reviews. This project is an integral part of the [Movie Counsel](https://movie-counsel.streamlit.app) web application, which empowers users to explore and discover movies tailored to their preferences.

**Key Features:**

- Sentiment Analyzer is implemented as a robust API using the FastAPI framework.
- The API is hosted on the Railway cloud platform, ensuring scalability, reliability, and ease of deployment.
- Sentiment analysis models are trained on a vast dataset comprising approximately 180k movie reviews sourced from IMDB.
- The reviews are scrapped from IMDB for both Hollywood and Bollywood releases from 2019 to September 2023 with help of Beautiful Soup.

### i) Data Preprocessing

The heart of any sentiment analysis model is the quality of its training data. Therefore, the dataset undergoes a rigorous preprocessing phase to optimize its quality for analysis.

**Data Cleaning and Preprocessing Tasks Include:**

- Correcting data formats to ensure uniformity and consistency with help of Pandas.
- Assigning review labels, i.e., classifying reviews as positive or negative based on the accompanying ratings.
- Removing special characters and symbols from the text, facilitating more accurate sentiment analysis.
- Applying word stemming techniques to further enhance the quality of the text data with help of nltk.
- visit the Google Colab notebooks in this [📁](https://drive.google.com/drive/folders/11Cm5Co2d-X9SrE8r7ANPu4-as3F_ik5Q?usp=drive_link) for detailed analysis.

### ii) Model Building

Sentiment Analyzer leverages state-of-the-art machine learning algorithms to create an accurate and robust sentiment classification model.

**Model Building Highlights:**

- Combination of machine learning algorithms, including Logistic Regression, Complement Naive Bayes, and XGBoost, to achieve precise sentiment classification.
- Incorporation of pretrained models such as roBERTa to expedite the training process and enhance overall performance.
- Continuous model evaluation and refinement to ensure the highest level of sentiment analysis accuracy.
- visit the Google Colab notebooks in this [📁](https://drive.google.com/drive/folders/11Cm5Co2d-X9SrE8r7ANPu4-as3F_ik5Q?usp=drive_link) for detailed analysis.

### iii) Web API

To make sentiment analysis accessible and user-friendly, Sentiment Analyzer provides a comprehensive web API. Users can interact with the API to gain insights into the sentiment of movie reviews.

**Key API Features:**

- Accepts HTTP POST requests containing movie reviews as input.
- Returns the probability of both negative and positive sentiments predicted by each model.
- Enables users to integrate sentiment analysis capabilities into their own applications and projects.

- Request
```
{
  "reviews": "This movie was absolutely fantastic! I loved every moment of it."
}
```
- Response - model:[negative score, positive score]
```
{
    "logistic_regression": {[0.15, 0.85]},
    "complement_naive_bayes": {[0.18, 0.82]},
    "xgboost": {[0.13, 0.87]}
}
```
## Web App
- Streamlit is used for building the web app and Stremlit Cloud is used for hosting the web app.

## 4. Find the demo below
https://github.com/peskyji/Recommender-System/assets/65287730/1bc03add-2872-466c-b8c5-9416469aff14