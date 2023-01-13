import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def read_and_clean_2021_2022(year):
  if year == 2021:
    df = pd.read_csv("2021.csv")
  if year == 2022:
    df = pd.read_csv("2022.csv")

  drop_cols = ['id', 'conversation_id', 'place', 'hashtags', 'cashtags', 'user_id', 
             'link', 'quote_url', 'geo', 'near', 'source', 'translate', 'trans_src', 'trans_dest', 'retweet_date','thumbnail', 'created_at', 'user_rt_id', 'user_rt',
             'retweet_id', 'reply_to', 'retweet', 'retweet_date', 'username', 'name', 'language', 'mentions', 'urls', 'photos', 'video', 'retweets_count', "replies_count"]
  df = df.drop(columns=drop_cols)

  df = df.rename(columns={'time':'timestamp'})
  df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S')
  # Extract the time from each timestamp
  df['time'] = df['timestamp'].dt.time
  df['time'] = df['time'].astype(str)
  df = df.drop(columns=['timestamp'])

  # Convert the 'date' and 'time' columns to datetime objects
  df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y-%m-%d %H:%M:%S')
  # Subtract 3 hours from each timestamp
  df['datetime'] = df['datetime'] - timedelta(hours=3)
  # Format the 'earlier_timestamp' column as a string
  df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')


  #Drop old times 
  df = df.drop(columns=['time', 'date'])


  #Take the new datetime and create new time and date columns with updated time
  df['datetime'] = pd.to_datetime(df['datetime'])
  df['date'] = df['datetime'].dt.strftime("%Y-%m-%d")
  df['time'] = df['datetime'].dt.strftime("%H:%M:%S")


  #Then we can finally drop the datetime column and timezone column as they are not needed anymore
  df = df.drop(columns=['datetime', 'timezone'])
  df['day']  = pd.to_datetime(df['date'], format='%Y-%m-%d').dt.weekday

  df = df.rename(columns={'likes_count':'nlikes'})

  return df
