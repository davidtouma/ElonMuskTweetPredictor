import os
import modal


LOCAL=False


if LOCAL == False:
   stub = modal.Stub()
   hopsworks_image = modal.Image.debian_slim().pip_install(["pandas", "tweepy"])
   @stub.function(image=hopsworks_image, schedule=modal.Period(days=1), secrets=[modal.Secret.from_name("HOPSWORKS_API_KEY"), modal.Secret.from_name("TWITTER_SECRETS")])
   def f():
       g()

def g():
  import pandas as pd
  import tweepy 
  import time
  #Pass in our twitter API authentication key

  consumer_key = os.environ["TWITTER_API_KEY"] #Your API/Consumer key 
  consumer_secret = os.environ["TWITTER_API_KEY_SECRET"]  #Your API/Consumer key 
  access_token = os.environ["TWITTER_ACCESS_TOKEN"] #Your API/Consumer key 
  access_token_secret = os.environ["TWITTER_ACCESS_TOKEN_SECRET"] #Your API/Consumer key 

  auth = tweepy.OAuth1UserHandler(
      consumer_key, consumer_secret,
      access_token, access_token_secret
  )

  username = 'elonmusk'
  no_of_tweets = 4 #Change this if you want more/fewer tweets

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
  except BaseException as e:
      print('Status Failed On,',str(e))
      time.sleep(3)
  print(tweets_df.head())


if __name__ == "__main__":
    if LOCAL == True:
        g()
    else:
        with stub.run():
            f()
