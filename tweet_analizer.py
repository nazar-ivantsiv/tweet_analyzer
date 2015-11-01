#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
twit analyzer

    analyzing twits by word ( how many tweets has this word)
    geo analyzing
    language analyzing
'''

import oauth2
import json
from auth_info import *
# File auth_info.py has to be in the same dir. Content:
#CONSUMER_KEY = <key>
#CONSUMER_SECRET = <secret>
#ACCESS_TOKEN = <token>
#ACCESS_TOKEN_SECRET = <token secret>


def oauth_req(url, key, secret, http_method='GET', post_body='', http_headers=None):
	'''
	Send authenticated Twiter HTTP request
	'''
	consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
	token = oauth2.Token(key=key, secret=secret)
	client = oauth2.Client(consumer, token)
	resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
	print('Server answer: {}'.format(resp['status']))
	return content

def analyze_by_word(word, tweets_to_get=100, language_geocode=('',''), result_type='mixed'):		# Also filters by language
	'''
	Finds the tweets with <word> in it.

	word 			- any word or tag to search for
	tweets_to_get 	- The number of tweets to return per query (max 100)
	language 		- ('en' - English, 'ar' - Arabic...)
	geocode		- (Example Values: 37.781157, -122.398720, 1mi) 1mi - range in miles (or km - kilometers)
	result_type 	- Specifies what type of search results you would prefer to receive
						(mixed, recent, popular)
	'''

	query = (
			'https://api.twitter.com/1.1/search/tweets.json?'
			'q={}&count={}&result_type={}'
			''.format(word, tweets_to_get, result_type) 
			)	

	if language_geocode[0] != '':
		query += '&lang={}'.format(language_geocode[0])
	if language_geocode[1] != '':
		query += '&geocode={}'.format(language_geocode[1])
	print(query)
	search_response = oauth_req( query, ACCESS_TOKEN, ACCESS_TOKEN_SECRET )
	response = json.loads(search_response)

	print('At least {} tweets below has \'{}\' word in it:'.format(len(response['statuses']), word))
	print_tweets(response)

def print_tweets(response):
	'''
	Prints tweets request nice and tidy

	response - dict of tweets (or error messages), generated from server response
	'''
	if 'statuses' in response.keys():
		for i, tweet in enumerate(response['statuses']):
			print('#{}:'.format(i))
			print( u' [tweet body]: {}'.format(tweet['text']) )
			print( ' [language]: {}'.format(tweet['lang']) )
			print( u' [location]: {}'.format(tweet['user']['location']) )
	else:	# if not a correct response
		for k in response.keys():
			print('\n')
			print(response[k])

# Search for tweets by word/tag with possibility to add LANGUAGE and GEOCODE filters


geocode = '37.781157,-122.398720,1mi'
# It is useful to add a function to get the geocode by location name (ex. Lviv)

word = raw_input('Word/tag to search for: ')

#analyze_by_word( word, 5, ('', geocode) )
analyze_by_word( word, 5, ('ja', '') )





'''
HELP
##########
Encription: vinigret - custom encoding (???)
############

import requests
res = requests.get('http://stackoverflow.com/questions/26000336')
#####################

import urllib, urllib2, json

url     = 'https://stage.wepayapi.com/v2/checkout/create'
headers = {
           'Content-Type': 'application/json',
           'User-Agent': 'Codecademy WePay Demo',
           'Authorization': 'Bearer STAGE_df1684a1c7b91f0de51b72e5890891b92d34e47fb3cb48d4dbd8d2a89fa253cc'
          }
params  = {
		   'account_id': 161624111,
		   'short_description': 'A brand new soccer ball',
		   'type': 'GOODS',
		   'amount': '24.95'
		  }
request = urllib2.Request(url, json.dumps(params), headers)

try:
	response = urllib2.urlopen(request, timeout=30).read()
	print json.loads(response)
except urllib2.HTTPError as e:
	print e
######################

Twitter oauth request:
Example request (Authorization header has been wrapped):

POST /oauth2/token HTTP/1.1
Host: api.twitter.com
User-Agent: My Twitter App v1.0.23
Authorization: Basic eHZ6MWV2RlM0d0VFUFRHRUZQSEJvZzpMOHFxOVBaeVJn
                     NmllS0dFS2hab2xHQzB2SldMdzhpRUo4OERSZHlPZw==Content-Type: application/x-www-form-urlencoded;charset=UTF-8
Content-Length: 29
Accept-Encoding: gzip

grant_type=client_credentials
######################

OAuth2 authentication & request:
#https://github.com/joestump/python-oauth2

import oauth2

def oauth_req(url, key, secret, http_method="GET", post_body='', http_headers=None):
	consumer = oauth2.Consumer(key='', secret='')
	token = oauth2.Token(key=key, secret=secret)
	client = oauth2.Client(consumer, token)
	resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
	return content

home_timeline = oauth_req( 'https://api.twitter.com/1.1/statuses/home_timeline.json', ACCESS_TOKEN, ACCESS_TOKEN_SECRET )

########################
Base64 encoding:

import base64
encoded = base64.b64encode('A014zUFPrlFlziRNiBc1EB2wH:5jG5reBuqy9rl1obfeomkVwvRHYd1du27gG6iqaaEzwd6x9aDo')

Base64 token:
QTAxNHpVRlBybEZsemlSTmlCYzFFQjJ3SDo1akc1cmVCdXF5OXJsMW9iZmVvbWtWd3ZSSFlkMWR1MjdnRzZpcWFhRXp3ZDZ4OWFEbw==

#######################

url     = 'https://api.twitter.com/oauth2/token'
headers = {
           'Content-Type': 'application/json',
           'User-Agent': 'Codecademy WePay Demo',
           'Authorization': 'Bearer STAGE_df1684a1c7b91f0de51b72e5890891b92d34e47fb3cb48d4dbd8d2a89fa253cc'
          }
params  = {
		   'account_id': 161624111,
		   'short_description': 'A brand new soccer ball',
		   'type': 'GOODS',
		   'amount': '24.95'
		  }
request = urllib2.Request(url, json.dumps(params), headers)

try:
	response = urllib2.urlopen(request, timeout=30).read()
	print json.loads(response)
except urllib2.HTTPError as e:
	print e
'''