import pandas as  pd
import streamlit as st
import requests
import json
import numpy as np
import plotly.graph_objects as go
import re
import joblib
from nltk.stem import PorterStemmer
import os

st.set_page_config(page_title='Movie Counsel',  layout='wide', page_icon=':clapper:')

def call_api():
    # response  = requests.post(url='https://sentiment-analysis-api.up.railway.app/predict', data = json.dumps({'reviews':reviews})).text
    response  = requests.post(url=st.secrets['API_URL'], data = json.dumps({'reviews':reviews}))
    print(response.status_code, response.text)
    return response

def load_models():
    abs_path = os.path.dirname(os.getcwd())
    print(abs_path)
    tfidf, lr, xgb, cnb = None, None, None, None
    try:
        tfidf =  joblib.load('Sentiment-Analysis-API/Models/tfidf.joblib')
        print(tfidf)
    except Exception as exp:
        print(f"problem in loading tfidf - {str(exp)}")
    try:
        lr =  joblib.load('Sentiment-Analysis-API/Models/lr.joblib')
        print(lr)
    except Exception as exp:
        print(f"problem in loading lr - {str(exp)}")
    try:
        xgb =  joblib.load('Sentiment-Analysis-API/Models/xgb.joblib')
        print(xgb)
    except Exception as exp:
        print(f"problem in loading xgb - {str(exp)}")
    try:
        cnb =  joblib.load('Sentiment-Analysis-API/Models/cnb.joblib')
        print(cnb)
    except Exception as exp:
        print(f"problem in loading cnb - {str(exp)}")
    return tfidf, lr, xgb, cnb

def preprocessing_task(review):
    ps = PorterStemmer()
    review = re.sub(r'[^A-Za-z\s]', '', review)
    print("Special Characters removed from review")
    review = re.sub(r' +', ' ', review)
    print("extra spaces removed")
    review = review.lower()
    print("Word Stemming stated...")
    review = " ".join([ps.stem(word) for word in review.split()])
    print("Stemming Completed")
    return review

def make_prediction(lr, cnb, xgb):
    lr_prob =  lr.predict_proba(X)[0]
    cnb_prob =  cnb.predict_proba(X)[0]
    xgb_prob =  xgb.predict_proba(X)[0]

    prob = {
                    'lr':[lr_prob[0], lr_prob[1]], 
                    'xgb':[xgb_prob[0], xgb_prob[1]],
                    'cnb':[cnb_prob[0], cnb_prob[1]]
            }
    return prob

def draw_pie_chart(labels, score):
    fig = go.Figure( data = [go.Pie(
                                labels=labels,
                                values = score,
                                name = "Score",
                                marker = dict(colors = ['#CF1020', '#004526']),
                                title = "Sentiment Score"
                        )])
    fig.update_traces(hole = .6, pull = [0,0.1], hoverinfo="label+percent+name", textfont_size=28)
    fig.update_layout(margin=dict(t=20, b=10, l=50, r=50), showlegend = False)
    st.write(fig)

def get_sentiment_text(score):
    if score[0] >= score[1]:
        st.info("Negative sentiment Detected")
    else:
        if score[1] >= 0.70:
            st.info("Postive Sentiment Detected")
        elif score[1] >= 0.60 and score[1] < 0.70:
            st.info("Mixed Sentiment Detected")
        else:
            st.info("Negative Sentiment Detected")
 
def produce_results(scores):
    if scores[0,1]-scores[1:,1].mean() > 0.10:
        scores[0,1] = scores[0,1]*0.85
        scores[0,0] = 1- scores[0,1]
    elif scores[0,0]-scores[1:,0].mean() > 0.10:
        scores[0,0] = scores[0,0]*0.85
        scores[0,1] = 1- scores[0,0]

    # st.write(scores)
    # st.write(scores.mean(axis=0))
    mean_scores = scores.mean(axis=0)

    selected_model = st.selectbox("", options=['All', 'Logistic Regression', 'XGBoost', 'Complement NB'], index=0)
    if selected_model == 'All':
        get_sentiment_text(mean_scores)
        draw_pie_chart(['Negative','Postive'], mean_scores)

    elif selected_model == 'Logistic Regression':
        get_sentiment_text(scores[0])
        draw_pie_chart(['Negative','Postive'], scores[0])

    elif selected_model == 'XGBoost':
        get_sentiment_text(scores[1])
        draw_pie_chart(['Negative','Postive'], scores[1])

    else:
        get_sentiment_text(scores[2])
        draw_pie_chart(['Negative','Postive'], scores[2])

cols = st.columns(5)
cols[2].image('images/logo7.gif')

st.header("Movie Review Sentiment Analyzer Tool")
reviews = st.text_area(label="", placeholder="Enter your review here")
# st.write(reviews)
# response = requests.session().post(url='http://127.0.0.1:8000/predict', data = json.dumps({'reviews':reviews}))
# st.write(response, response.text)
temp = re.search(r'^[a-zA-Z0-9\s][a-zA-Z]+', reviews)
if(temp!=None and len(re.sub(' +',' ',reviews).strip().split())<3):
    st.warning("!!! Please type at least three words, Entering a proper sentece is recommened to precisely analyse the sentiment !!!")

elif temp != None:
    response = call_api()
    if(response.status_code == 200):
            
        scores= json.loads(json.loads(response.text))
        scores = np.array([scores['lr'], scores['xgb'], scores['cnb']])
        produce_results(scores)
        
    elif(response.status_code >= 500):
        st.toast("🤷 Server is temporarily down, fetching results locally")
        tfidf, lr, xgb, cnb = load_models()
        review = preprocessing_task(reviews)
        X =  tfidf.transform(pd.Series(review))
        prob = make_prediction(lr, cnb, xgb)
        scores = np.array([prob['lr'], prob['xgb'], prob['cnb']])
        produce_results(scores)
    else:
        st.error(f"oops error occured with response code {response.status_code}")
