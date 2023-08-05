import json
import requests
import traceback
from bs4 import BeautifulSoup

__version__ = "1.0.4"
__author__  = "Francis Taylor"

class OnInstagram:
	def __init__(self, obj):
		self.name      = obj.name
		self.username  = obj.username
		self.followers = obj.followers
		self.following = obj.following
		self.picture   = obj.picture
		self.website   = obj.website
		self.bio       = obj.bio
		self.posts     = obj.posts

class Profile:
	def __init__(self, username):
		html = requests.get(f"https://bibliogram.pussthecat.org/u/{username}")
		soup = BeautifulSoup(html.text, 'html.parser')
		
		self.picture   = f'''https://bibliogram.pussthecat.org{soup.find_all("img", attrs={'class':'pfp'})[0].get('src')}'''
		self.name      = soup.find_all('h1', attrs={'class':'full-name'})[0].get_text()
		self.username  = soup.find_all('h2', attrs={'class':'username'})[0].get_text()
		try:   self.bio = soup.find_all('p', attrs={'class':'structured-text bio'})[0].get_text()
		except:self.bio = None
		try:   self.website= soup.find_all('p', attrs={'class':'website'})[0].get_text()
		except:self.website=None
		counters  = soup.find_all('div', attrs={'class':'profile-counter'})
		self.posts     = counters[0].get_text()
		self.following = counters[1].get_text()
		self.followers = counters[2].get_text()
	

	def on_dict(self, dumps=False, indent=4):
		dictionary = dict(posts=self.posts, bio=self.bio, website=self.website, name=self.name, username=self.username, followers=self.followers, following=self.following, picture=self.picture)
		if dumps:
			dictionary = json.dumps(dictionary, indent=indent)
		return dictionary

	def on_obj(self):
		return OnInstagram(self)

