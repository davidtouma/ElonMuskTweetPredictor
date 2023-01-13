# ElonMuskTweetPredictor
Project In Scalable Machine Learning

# Introduction - Using GPT-2 to generate tweets similar to Elon Musk


The CSV file (cleanedTweetData) is a cleaned version of the data from https://www.kaggle.com/datasets/ayhmrba/elon-musk-tweets-2010-2021

In this repository you will find both notebooks and python scripts. The purpose of this is to use the notebook as "tutorials" while the scripts do not include much text but can be used quickly. 

# Step 1 - Handling historical data

As previously mentioned, we got our historical data from https://www.kaggle.com/datasets/ayhmrba/elon-musk-tweets-2010-2021. The files from this website can be found in the folder "Uncleaned Elon Data".

In the notebook CleanElonTweetDataNotebook.ipynb, a step by step "tutorial" is done so that you can get an intuiton of what was done when cleaning the data. If you do not want to use it you can look at the other notebook feature_engineering_scripts_notebook.ipynb. There I define two functions that do the same thing I did in the first notebook and then upload it to our feature store in Hopsworks

The script feature_engineering_script.py, is a script that uploads the data to Hopswork's feature store

# Step 2 - Finding live data.

For the second task, this project looks into using live data, to extend our dataset but also be used later for our machine learning application. For this, we were granted access to the Twitter API, which we then could use to scrape tweets and other relevant data. 

With the twitter API, we created a script that scrapes tweets and also process the data into a dataframe that suits our feature store from the previous step. 

By using the platform Modal (visit https://modal.com/), we can deploy our script online and specify in the script to scrape four tweets and insert them to our data storage in Hopsworks. This process can be found in the script modal_script.py'

The test_modal_script.py script, was used as an initial test when exploring how to deploy scripts to modal. It is a simple script that prints the data we have scraped from Twitter


# Step 3 - Fine Tuning a GPT-2 model for text generation/Huggingface
....


# Step 4 - UI using Huggingface
....


# NOTE!!!!

To be able to use some of the scripts, you will need to have access to different API keys, such as four different keys from the Twitter API, an API key from Hopsworks,  an access token from Huggingface, and generate a token from Modal.


