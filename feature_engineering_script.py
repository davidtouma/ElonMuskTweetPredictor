import os
from historic_data_script21_22 import read_and_clean_2021_2022
from historic_data_script_20 import read_and_clean_2020


def g():
    import hopsworks
    import pandas as pd

    #We use our scripts that reads and clean the csv files
    df_20 = read_and_clean_2020()
    df_21 = read_and_clean_2021_2022(2021)
    df_22 = read_and_clean_2021_2022(2022)
    frames = [df_20, df_21, df_22]
    #Concatenate the dfs into one df
    concat_df = pd.concat(frames)

    feature_list = []

    project = hopsworks.login()
    fs = project.get_feature_store()

    for features in concat_df.columns:
        feature_list.append(features)

    em_tweet_fg = fs.get_or_create_feature_group(
        name="elon_musk_tweets_modal",
        version=1,
        primary_key= feature_list,
        description = "Elon Musks Tweets from 2010-2022")
    em_tweet_fg.insert(concat_df, write_options={"wait_for_job" : False})


if __name__ == "__main__":
    g()