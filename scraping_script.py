import tweepy
import pandas as pd
import time


consumer_key = "XXXX" #Your API/Consumer key 
consumer_secret = "XXXX" #Your API/Consumer Secret Key
access_token = "XXXX"    #Your Access token key
access_token_secret = "XXXX" #Your Access token Secret key

def scrape_tweets(username, no_of_tweets, consumer_key, consumer_secret, access_token, access_token_secret):
  #Pass in our twitter API authentication key
  auth = tweepy.OAuth1UserHandler(
      consumer_key, consumer_secret,
      access_token, access_token_secret
  )


  #Instantiate the tweepy API
  api = tweepy.API(auth, wait_on_rate_limit=True)
  try:
      #The number of tweets we want to retrieved from the user
      tweets = api.user_timeline(screen_name=username, count=no_of_tweets)
      
      #Pulling Some attributes from the tweet
      attributes_container = [[tweet.created_at, tweet.favorite_count, tweet.text] for tweet in tweets]

      #Creation of column list to rename the columns in the dataframe
      columns = ["Date Created", "Number of Likes", "Tweet"]

      
      #Creation of Dataframe
      tweets_df = pd.DataFrame(attributes_container, columns=columns)
      tweets_df["date"] = tweets_df["Date Created"].dt.date
      tweets_df["date"] = tweets_df["Date Created"].dt.strftime("%Y-%m-%d")
      tweets_df["time"] = tweets_df["Date Created"].dt.strftime("%H:%M:%S")

      tweets_df['day'] = pd.to_datetime(tweets_df['date'], format='%Y-%m-%d').dt.weekday


      tweets_df = tweets_df.rename(columns={'Tweet':'tweet', "Number of Likes": "nlikes"})
      tweets_df = tweets_df.drop(columns=['Date Created'])
      tweets_df = tweets_df[tweets_df['nlikes'] != 0] #Removes all rows where nlikes == 0. As those are retweets which we do not want

      return tweets_df
  except BaseException as e:
      print('Status Failed On,',str(e))
      time.sleep(3)

tweets = scrape_tweets("elonmusk", 4, consumer_key, consumer_secret, access_token, access_token_secret)
print(tweets.head())