from flask import Flask,render_template
from flask_ask import  Ask,statement,question,session
import json
import requests
import time
import unidecode


app = Flask(__name__)

ask = Ask(app,"/reddit_reader")

def get_headline():
	user_pass_dict = { 'user' : 'darktrooper25',
					   'passwd':'darktrooper25',
					   'api_type':'json'  }
	sess = requests.Session()
	sess.headers.update({'User-Agent':'testing v1 alexa'})
	sess.post('https://www.reddit.com/api/login',data = user_pass_dict)
	time.sleep(1)
	url = 'https://reddit.com/r/india_tourism/.json?limit=3'
	html = sess.get(url)
	data = json.loads(html.content.decode('utf-8'))
	titles = [unidecode.unidecode(listing['data']['title']) for listing in data['data']['children']]
	titles = '... '.join([i for i in titles])
	return titles




@app.route('/')
def homepage():
	return "hi how are you doing"

@ask.launch
def start_skill():
	welcome_message = "namaste ..shall we begin your journey of healing?"
	return question(welcome_message)

@ask.intent("yesintent")
def share_headlines():
	headlines = get_headline()
	headline_msg = 'to get you started here are some facts {}'.format(headlines)
	return statement(headline_msg)

@ask.intent("nointent")
def no_intent():
	bye_text = 'bruh come on'
	return statement(bye_text)


if __name__ == "__main__":
	app.run(debug=True)	