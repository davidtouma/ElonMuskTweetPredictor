import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def read_and_clean_2020():
  df_20 = pd.read_csv("2020.csv")
  
  #Drop unnecessary columns
  drop_cols = ['Unnamed: 0', 'id', 'conversation_id', 'place', 'hashtags', 'cashtags', 'user_id','user_id_str', 
            'link', 'quote_url', 'search', 'geo', 'near', 'source', 'translate', 'trans_src', 'trans_dest', 'retweet_date','thumbnail', 'created_at', 'user_rt_id', 'user_rt',
            'retweet_id', 'reply_to', 'hour', 'username', 'name', 'language', 'nretweets', 'nreplies', 'urls', 'photos', 'video', 'retweet']
  df_20 = df_20.drop(columns = drop_cols)
  #For convenience, we rename date column to datetime since that is what it is
  df_20 = df_20.rename(columns={'date':'datetime'})
  #Fix the time so that it follows swedish time
  df_20['datetime'] = pd.to_datetime(df_20['datetime'])
  df_20['datetime'] = df_20['datetime'] + timedelta(hours=1)
  df_20['date'] = df_20['datetime'].dt.strftime("%Y-%m-%d")
  df_20['time'] = df_20['datetime'].dt.strftime("%H:%M:%S")
  #Datetime and timezone columns are not needed now so we drop them
  df_20 = df_20.drop(columns=['datetime', 'timezone'])
  
  return df_20