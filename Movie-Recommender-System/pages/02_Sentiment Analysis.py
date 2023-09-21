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
    response  = requests.post(url='https://sentiment-analysis-api-szr4.onrender.com', data = json.dumps({'reviews':reviews}))
    return response

def load_models():
    abs_path = os.path.dirname(os.getcwd())
    tfidf, lr, xgb, cnb = None, None, None, None
    try:
        tfidf =  joblib.load(f'{abs_path}/Sentiment-Analysis-API/Models/tfidf.joblib')
        print(tfidf)
    except Exception as exp:
        print(f"problem in loading tfidf - {str(exp)}")
    try:
        lr =  joblib.load(f'{abs_path}/Sentiment-Analysis-API/Models/lr.joblib')
        print(lr)
    except Exception as exp:
        print(f"problem in loading lr - {str(exp)}")
    try:
        xgb =  joblib.load(f'{abs_path}/Sentiment-Analysis-API/Models/xgb.joblib')
        print(xgb)
    except Exception as exp:
        print(f"problem in loading xgb - {str(exp)}")
    try:
        cnb =  joblib.load(f'{abs_path}/Sentiment-Analysis-API/Models/cnb.joblib')
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
    # print(mean_scores)

    if mean_scores[0] >= mean_scores[1]:
        st.info("Negative sentiment Detected")
    else:
        if mean_scores[1] >= 0.70:
            st.info("Postive Sentiment Detected")
        elif mean_scores[1] >= 0.60 and mean_scores[1] < 0.70:
            st.info("Mixed Sentiment Detected")
        else:
            st.info("Negative Sentiment Detected")

    fig = go.Figure( data = [go.Pie(
                                labels=['Negative','Postive'],
                                values = mean_scores,
                                name = "Score",
                                marker = dict(colors = ['#CF1020', '#004526'])
                        )])
    fig.update_traces(hole = .55, pull = [0,0.1], hoverinfo="label+percent+name", textfont_size=28)
    fig.update_layout(margin=dict(t=20, b=10, l=50, r=50))

    st.write(fig)


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
        st.warning("Server is temporarily down, fetching results locally")
        tfidf, lr, xgb, cnb = load_models()
        review = preprocessing_task(reviews)
        X =  tfidf.transform(pd.Series(review))
        prob = make_prediction(lr, cnb, xgb)
        scores = np.array([prob['lr'], prob['xgb'], prob['cnb']])
        produce_results(scores)
    
