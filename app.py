from flask import Flask, request, render_template, redirect, flash
from flask_table import Table, Col
import tweepy as tw

app = Flask(__name__)

# keys for twitter access:
consumer_key = 'zx15WTQ5JL0Z6vn6OjHFu8mT0'
consumer_secret = 'TqlEBrFCthsofSmM5wWfzkEo45vXWN9z9ML19n5ApueaC7Kaj0'
access_token = '22489193-KvaYnRzomWwY6WYmBmToXqwwOfD0npRWMGyUnKhzX'
access_token_secret = 'EWpHq0qNFSgsBIGbIPmdzfb40wpuHwNqEGt7qHA3WqCA2'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

# Define the search term and the date_since date as variables
search_words = ""
date_since = "2018-11-16"

class Results(Table):
  screen_name = Col('Screen Name')
  created_at = Col('Tweet Time')
  text = Col('Tweet Text')

@app.route("/")
def main():
   return render_template('index.html') 



@app.route('/search', methods = ['POST'])
def search():

   # read the posted value from the UI
   search_words = request.form['inputSearch']
   try:
      search_length = int(request.form['inputLength'])
   except ValueError:
      search_length = 5
  
   if search_length < 1:
      search_length = 5
   elif search_length > 100:
      search_length = 100
 
   if search_words:
      # Collect tweets
      tweets = tw.Cursor(api.search,q=search_words,lang="en",since=date_since).items(search_length)

      results = []
      print('------ Tweets ------')
      # Iterate on tweets
      for tweet in tweets:
         print(tweet.user.screen_name, ',', tweet.user.location, ',', tweet.created_at, ',',  tweet.text)
         results.append([tweet.user.screen_name, tweet.user.location, tweet.created_at, tweet.text])

      # table = Results(results)
      # table.border = True
      # return render_template('results.html', table=table)
      return render_template('results.html', table=results)

   else:
      # flash("No search words specified!")
      return redirect('/')

   # return render_template('search.html')
   print("done")
   return render_template('search.html') 

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)
