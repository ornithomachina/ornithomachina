import tweepy
import config
# Setting up API access
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

# Creating an api object
api = tweepy.API(auth)

with open('test_group.txt', 'r') as f:
    test_list = [line.rstrip('\n') for line in f]
f.close()

with open('control_group.txt', 'r') as f:
    control_list = [line.rstrip('\n') for line in f]
f.close()

print(test_list)
print(control_list)

def sumEngagement(list):
    quote_sum = 0
    reply_sum = 0
    retweet_sum = 0
    favorite_sum = 0
    if len(list) > 0:
        x = api.statuses_lookup(list)
        for status in x:
            print(status)
            print('\n')

            status = status._json
            print(status)
            print('\n')

            print(status['id'])
            tweet_url = f"https://twitter.com/user/status/{status['id']}"
            print(tweet_url)

            #print(x.id)
            #tweet_url = f"https://twitter.com/user/status/{x.id}"

            #quote_sum += status['quote_count']
            #reply_sum += status['reply_count']
            retweet_sum += status['retweet_count']
            favorite_sum += status['favorite_count']

    print('Quotes: ' + str(quote_sum) + '\n')
    print('Replies: ' + str(reply_sum) + '\n')
    print('Retweets: ' + str(retweet_sum) + '\n')
    print('Favorites: ' + str(favorite_sum) + '\n')





print(sumEngagement(test_list))
print('====Test list====')
print('\n')

print(sumEngagement(control_list))
print('====Control list====')
print('\n')