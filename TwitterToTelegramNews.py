import tweepy
import time
import DataAccess as dal
import requests
import feedparser
from datetime import timedelta, datetime
from dateutil import parser

def main():
    data = dal.getData()

    BOT_TOKEN = data['botToken']
    CHANNEL_ID = data['channelId']

    twitterApi = getTwitterAPI(data)
    lastId = data['lastId']
    tweets = []

    print('Begining the loop...' + '\n')

    while True:
        try:
            print('Checks for tweets...' + '\n')
            tweets = twitterApi.home_timeline(since_id = lastId)
            if tweets:
                print('Tweets found!' + '\n')
                for tweet in tweets:
                    message = getMessage(tweet)
                    send_message(message, BOT_TOKEN, CHANNEL_ID)
                    print('telegramed!\n')            
                lastId = tweets[0].id
                data['lastId'] = lastId
                dal.setData(data)
            else:
                print('No new tweets!' + '\n')
        except tweepy.RateLimitError as e:
            lastId = tweets[0].id
            data['lastId'] = lastId
            dal.setData(data)
            print('We hit rate limit...' + '\n')
            print(str(e))
        except Exception as e:
            lastId = tweets[0].id
            data['lastId'] = lastId
            dal.setData(data)
            print('We have a problem!' + '\n')
            print(str(e))

        print('Now I\'m sleeping for a minute...' + '\n')
        time.sleep(60)

def send_message(message, BOT_TOKEN, CHANNEL_ID):
    requests.get(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHANNEL_ID}&text={message}&parse_mode=html')

def getTwitterAPI(data):
    # Authenticate to Twitter
    auth = tweepy.OAuthHandler(data['apiKey'], data['apiSecret'])
    auth.set_access_token(data['accessToken'], data['accessSecret'])
    return tweepy.API(auth)

def getMessage(tweet):
    message = '<a href="twitter.com/'
    message += tweet.user.screen_name
    message += '">'
    message += tweet.user.name
    message += '</a>:<br><br>'
    message += tweet.text
    return message

if __name__ == '__main__':
    main()
