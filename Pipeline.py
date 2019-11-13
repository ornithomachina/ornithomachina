# If you fork this project, you will need to set up your own Twitter App and generate API keys and access tokens
import tweepy
import config   # config.py not included in this public repo
from newspaper import Article
import pickle
import numpy as np
import pandas as pd
import math


# Setting up API access
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

# Creating an api object
api = tweepy.API(auth)

# Loading model and vectorizers from pickle
model = pickle.load(open('model.pickle', 'rb'))
title_vectorizer = pickle.load(open('title_vectorizer.pickle', 'rb'))
body_vectorizer = pickle.load(open('body_vectorizer.pickle', 'rb'))

# Prefix titles just like in the model processor
def prefix(string, prefix):
    spl_str = string.split()
    result = []
    pref_str = ''
    for x in spl_str:
        pref_str = pref_str + (prefix + x) + ' '
    result.append(pref_str)
    return result

def getResponse(prediction):
    response = f"Our model predicts that there is a {prediction} chance that this story is false, based on the characteristics of the article text. " \
               f"\nWe encourage checking other sources!"

    return response

class Engager:
    test_group = []
    control_group = []
    toggle = True
    def engagementTest(status):
        # Hacky way to split into control and test groups
        if toggle is True:
            print('GOING INTO CONTROL')
            control_group.append(status)
            toggle = not toggle
            return False
        else:
            print('GOING INTO TEST')
            test_group.append(status)
            toggle = not toggle
            return True


# Override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        result_dict = status._json

        # Check if this tweet is original and in english: not quoting anyone, not replying to a tweet, not a retweet, and lang param is english
        if ('quoted_status_id' not in result_dict) and (status.in_reply_to_status_id is None) and ('RT @' not in status.text) and (result_dict['lang'] == 'en'):
            try:

                entities = result_dict['entities']
                #print(entities)
                #print(entities.keys())
                urls = entities['urls']
                #print(urls)
                expanded_url = urls[0]['expanded_url']
                if 'twitter.com' not in expanded_url:
                    #print(result_dict)
                    article = Article(url=expanded_url)
                    article_title = 'NO TITLE YET'
                    article_text = 'NO TEXT YET'
                    try:
                        # Use newspaper library to access elements of the article
                        article.download()
                        article.parse()
                        article_text = article.text
                        article_title = article.title

                        # Begin ML analysis
                        article_title_prefixed = prefix(article_title, 'title_')
                        article_title_vect = title_vectorizer.transform(article_title_prefixed)
                        article_text_vect = body_vectorizer.transform([article_text])


                        article_title_vect = article_title_vect.toarray()
                        article_text_vect = article_text_vect.toarray()


                        test = np.concatenate((article_title_vect, article_text_vect), axis=1)


                        test_pred = model.predict(test)


                        test_proba = model.predict_proba(test)


                        log_prob = math.log(test_proba[0][1]/test_proba[0][0])
                        if log_prob < -0.5:
                            print(status.text + '\n')
                            tweet_url = f"https://twitter.com/user/status/{status.id}"
                            print('LINK TO TWEET: ' + tweet_url)
                            print('*********\n')
                            print('URL IN TWEET: ' + expanded_url)

                            print('TITLE: ' + article_title + '\n')
                            print('TEXT: ' + article_text + '\n')

                            print('====ANALYSIS====\n')
                            print(article_title_vect)
                            print(article_title_vect.shape)
                            print(article_text_vect)
                            print(article_text_vect.shape)

                            print('FULL: ')
                            print(test)

                            print('PREDICTION: ')
                            print(test_pred)
                            print('\n')

                            print('LABEL PROBABILITIES: ')
                            print(test_proba)
                            print(test_proba[0])
                            print('\n')

                            print('LOG PROBABILITY: ')
                            print(log_prob)
                            print('\n')

                            if(engagementTest(status)):
                                print('RESPONSE: \n')
                                response = test_proba[0][0]
                                response = '{:,.2%}'.format(response)
                                print(getResponse(response))


                    except Exception as e:
                        print(e)
                        print('ERROR\n')

            except Exception as e:
                print(e)
                print('no url')

    '''
    def on_data(self, raw_data):
        return
    '''


# Creating stream object, with the api object auth attribute and the streamListener instance as parameters
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# Create engagement object for later analysis
myEngager = Engager()

# For some reason, this retweet filtering doesn't seem to work as expected
print(myStream.filter(track=['ukraine', 'trump', 'pelosi', 'filter:links', '-filter:retweets']))
