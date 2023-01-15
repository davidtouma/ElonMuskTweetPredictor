#batch inference pipeline
import os
import modal

LOCAL = False

if LOCAL == False:
   stub = modal.Stub()
   hopsworks_image = modal.Image.debian_slim().pip_install(["hopsworks","joblib","transformers", "torch"])
   @stub.function(image=hopsworks_image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
   def f():
       g()


def g():
  import pandas as pd
  from datetime import datetime
  import transformers
  import hopsworks
  from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

  project = hopsworks.login()
  fs = project.get_feature_store()
  
  #Get the latest inserted tweet from our feature group
  tweet_fg = fs.get_feature_group(name="elon_musk_tweets_modal", version=1)
  tweet_df = tweet_fg.read()
  latest_tweet = tweet_df["tweet"].iloc[-1] #Latest Original Tweet from EM
  split_latest_tweet = latest_tweet.split()
  first_two_strings = split_latest_tweet[:2]
  #Prompt that we input to our model
  prompt_predict = first_two_strings[0] + " " + first_two_strings[1]
  
  #Get the model from huggingface
  tokenizer = AutoTokenizer.from_pretrained("davidt123/Final-GPT-2-Elon-Model")
  model = AutoModelForCausalLM.from_pretrained("davidt123/Final-GPT-2-Elon-Model")
  generator = pipeline('text-generation', model=model, tokenizer=tokenizer)
  text_list = generator(prompt_predict, max_length=280, num_return_sequences=1)
  predicted_tweet = [d.get('generated_text') for d in text_list][0] #Predicted tweet based by the first two words from the original tweet

  #Generate a daily random tweet
  random_prompt = ""
  text_list = generator(random_prompt, max_length=280, num_return_sequences=1)
  random_tweet = [d.get('generated_text') for d in text_list][0]

  #We create a new feature group for monitoring our results
  monitor_fg = fs.get_or_create_feature_group(
      name="em_gpt_monitor",
      version=1,
      primary_key= ["datetime"],
      description = "Generated tweets by our GPT-2 model"
  )
  now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
  data = {
      'original_tweet' : [latest_tweet],
      'predicted_tweet' : [predicted_tweet],
      'random_tweet' : [random_tweet],
      'datetime' : [now]
  }
  monitor_df = pd.DataFrame(data)
  monitor_fg.insert(monitor_df, write_options={"wait_for_job" : False})


if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        with stub.run():
            f()