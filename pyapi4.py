from flask import Flask, render_template, request
import random
import flask
import fasttext
import tweepy
import json
#twitter login
try:
    # Consumer keys and access tokens, used for OAuth
    consumer_key = 'RYQlJ5EYXslMmqgPQIZYp6LkS'
    consumer_secret = 'q3CiYTWfWa1egNuuMZehWCpwDSCpZHZle2WDmrYULqUi9BS11b'
    access_token = '74141815-NGJy15QAvpq799QJbvj4BuDjcOJ5vuDsoMW0Mqku3'
    access_token_secret = 'GqS5T7fDn22TOScuu7N06iERYuVMsS7a8jPtIrN9weTtg'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    # Creation of the actual interface, using authentication
    api = tweepy.API(auth)
except:
    print("error or already logged in")

classifier = fasttext.load_model("nestle_model_py2.bin")
app = Flask(__name__, template_folder='templates1')

@app.route('/', methods=['GET','POST'])
def samplefunction():
    if request.method == 'GET':
        return render_template('new.html')
    if request.method == 'POST':
        text = [request.form['human']]
        text1 = str(text) + " -filter:retweets" 
        fetched_tweets = api.search(text1, count = 10 , lang = 'en')
        pred_labels = []
        pred_prob = []
        tweet_id = []
        dict1 = {}
        for tweets in fetched_tweets:
            pred = []
            prob = []
            pred1 = str(classifier.predict_proba([tweets.text], k = 4)[0][0]).replace("('__label__","").split(",")[0].replace("'","").lower().replace("/","_")
            pred2 = str(classifier.predict_proba([tweets.text], k = 4)[0][1]).replace("('__label__","").split(",")[0].replace("'","").lower().replace("/","_")
            pred3 = str(classifier.predict_proba([tweets.text], k = 4)[0][2]).replace("('__label__","").split(",")[0].replace("'","").lower().replace("/","_")
            pred4 = str(classifier.predict_proba([tweets.text], k = 4)[0][3]).replace("('__label__","").split(",")[0].replace("'","").lower().replace("/","_")
            prob1 = int(round(float(str(classifier.predict_proba([tweets.text], k = 4)[0][0]).replace("('__label__","").split(",")[1].replace(" ","").replace(")",""))*100,0))
            prob2 = int(round(float(str(classifier.predict_proba([tweets.text], k = 4)[0][1]).replace("('__label__","").split(",")[1].replace(" ","").replace(")",""))*100,0))
            prob3 = int(round(float(str(classifier.predict_proba([tweets.text], k = 4)[0][2]).replace("('__label__","").split(",")[1].replace(" ","").replace(")",""))*100,0))
            prob4 = int(round(float(str(classifier.predict_proba([tweets.text], k = 4)[0][3]).replace("('__label__","").split(",")[1].replace(" ","").replace(")",""))*100,0))
            pred = [pred1, pred2, pred3, pred4]
            prob = [prob1, prob2, prob3, prob4]
            pred_labels.append(pred)
            pred_prob.append(prob)
            tweet_id.append(tweets.id_str)
            
        list1=[]
        dict1={}
        for i,j,k in zip(pred_labels,pred_prob,tweet_id):
            dict1[k]=dict(zip(i,j))
        bot = str(classifier.predict(text)[0][0]).replace("__label__","")
        print(dict1);
        #dict_final=json.dump(dict1)
        return flask.jsonify(dict1)
        #return render_template('new.html', bot=bot, human = text[0], json_v = dict1,pred1 = pred1, pred2 = pred2, pred3 = pred3, pred4 = pred4, prob1 = prob1, prob2 = prob2, prob3 = prob3, prob4 = prob4)




app.run(debug=True)


