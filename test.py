import twitter
import config
import MySQLdb
import time
# from bson import json_util as jsonb
from pymongo import MongoClient


class Crawler:
	def __init__(self):

		# client = MongoClient('127.0.0.1', 27017)
		# db_name = 'twitter'
		# db = client[db_name]
		# collect_all = db['tweets_all']

		# # for i in range(10, 100):
		# # 	print str(i) + "................................................."
		# # 	collect = db['tweets_' + str(i)]
		# # 	for item in collect.find():      
	 # #   			collect_all.insert_one(item)
			
		# # return

		# collect = db['tweets_76']
		# time1 = time.time()
		# print collect.find({"user_id":76}).count()
		# time2 = time.time()
		# print time2 - time1
		# return
		a = [1, 2, 3]
		print a
		self.test(a)
		print a
		return

		api = []
		self.apiCount = 28
		for i in range(self.apiCount):
			api.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))
		# user_id = 622567875
		# user = api[0].GetUsersSearch(term = 'marco')
		# for u in user:
		# 	print u

		# tweets = api[0].GetUserTimeline(screen_name = 'marcohan2333',trim_user = True, count = 200)
		user = api[0].GetUser(user_id = 15049217)
		print user
		# print tweets[3]
		return

		user.is_translator = True
		is_translator = 0
		if hasattr(user, "is_translator"):
			is_translator = 1 if user.is_translator else 0

		print is_translator
		return
		name = user.name.replace("'","\\'")
		location = user.location.replace("'","\\'") if user.description else ''
		description = user.description.replace("'","\\'") if user.description else ''
		protected = 1 if user.protected else 0
		verified = 1 if user.verified else 0
		geo_enabled = 1 if user.geo_enabled else 0
		listed_count = user.listed_count if user.listed_count else 0
		default_profile_image = 1 if user.default_profile_image else 0 

		sql = """INSERT INTO user_1(user_id, screen_name, name, location, created_at, description, statuses_count, friends_count, 
				followers_count, favourites_count, lang, protected, time_zone, verified, utc_offset, geo_enabled, listed_count,
				is_translator, default_profile_image, profile_background_color, profile_sidebar_fill_color, profile_image_url, crawler_date) VALUES
				('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s', %d, '%s', %d, '%s', %d, %d, %d, %d,
				'%s', '%s', '%s', '%s')""" % (user_id, user.screen_name, name, location, user.created_at, description, user.statuses_count, \
				user.friends_count, user.followers_count, user.favourites_count, user.lang, protected, user.time_zone, verified, \
				user.utc_offset, geo_enabled, listed_count, is_translator, default_profile_image, user.profile_background_color, \
				user.profile_sidebar_fill_color, user.profile_image_url, time.strftime('%Y-%m-%d',time.localtime(time.time()))) 

		print sql

		return




		client = MongoClient('127.0.0.1', 27017)
		db_name = 'twitter'
		db = client[db_name]
		collect = db['tweet']


		for i in range(10, 100):
			db.createCollection("tweet_" + str(i))

		return
		


		self.api = api
		tweet = api[0].GetStatus(status_id = 603755837782269953)
		print tweet
		return
		# self.getUserTweets('realDonaldTrump')
		tweets = api[0].GetUserTimeline(screen_name = 'realDonaldTrump', max_id = 711042337158340608, trim_user = True, count = 200)
		print tweets[0]
		tweets = api[0].GetUserTimeline(screen_name = 'realDonaldTrump', max_id = 711042337158340608, count = 200)
		print tweets[0]
		# self.getUserTweetsRev('taylorswift13')
		return

		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		cursor = db.cursor()
		# self.cursor = cursor
		# self.db = db
		# return

		sql = "select user_id from user_all where statuses_count > 100 and lang = 'en' and protected = 1"
		try:
			cursor.execute(sql)
			info = cursor.fetchall()
		except:
			return 

		for ii in info:
			try:
				tweets = api[0].GetUserTimeline(user_id = ii[0], count = 20)
				print ii[0] + " finished..."
			except Exception as e:
				print e
				print ii[0] + " failed"
				continue
	
		return


		name_list = ['floydmayweather', 'jp_books', 'robertdowneyjr', 'taylorswift13', 
				'cristiano', 'messi10stats', 'd_copperfield', 'ryanseacrest', 'jldaily', 'EyeOfJackieChan', 
				'kobebryant', 'leodicaprio', 'neymarjr', 'jimmybuffett', 'srbachchan', 'billgates', 
				'tim_cook', 'barackobama', 'hillaryclinton', 'theterminal']
		api = []
		self.apiCount = 28
		for i in range(self.apiCount):
			api.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))

		client = MongoClient('127.0.0.1', 27017)
		db_name = 'twitter'
		db = client[db_name]
		collect = db['tweet']
		tweets = api[0].GetUserTimeline(screen_name = 'marcohan2333', max_id = 711042337158340608, count = 200)
		
		for tt in tweets:
			coordinates = None
			if tt.coordinates != None:
				coordinates = {
					"coordinates":tt.coordinates.coordinates,
					"type": tt.coordinates.type
				}

			tweet = {
				# 'contributors': tt.,
				'coordinates': coordinates,  # Coordinates
				'created_at': tt.created_at, # String
				# 'current_user_retweet': None,
				'favorite_count': tt.favorite_count, # int
				# 'favorited': tt.favorited,
				'filter_level': tt.filter_level if hasattr(tt, 'filter_level') else '', # String
				# 'geo': tt.geo,
				'hashtags': map(lambda x: x.text, tt.hashtags), # {'0': ,'1':}
				'_id': tt.id_str, # String
				# 'id_str': tt.id_str,
				'in_reply_to_screen_name': tt.in_reply_to_screen_name if hasattr(tt, 'in_reply_to_screen_name') else '', # String
				'in_reply_to_status_id': tt.in_reply_to_status_id_str if hasattr(tt, 'in_reply_to_status_id_str') else '', # String
				'in_reply_to_user_id': tt.in_reply_to_user_id_str if hasattr(tt, 'in_reply_to_user_id_str') else '', # String
				'lang': tt.lang, # String
				# 'media': tt.media,
				'place': tt.place, # Place
				'possibly_sensitive': tt.possibly_sensitive, # Boolean
				'retweet_count': tt.retweet_count, # int
				# 'retweeted': tt.retweeted,
				# 'retweeted_status': tt.retweeted_status,
				# 'scopes': tt.scopes, # Object
				'source': tt.source, # String
				'text': tt.text, # String
				# 'truncated': tt.truncated,
				# 'urls': tt.urls, # []
				'user_id': tt.user.id, # int
				'user_mentions': map(lambda x: x.id, tt.user_mentions), # []
				'withheld_copyright': tt.withheld_copyright, # Boolean
				'withheld_in_countries': tt.withheld_in_countries, # Array of String
				'withheld_scope': tt.withheld_scope, #String
			}
			collect.insert_one(tweet)
			# return
		return
		
	def test(self, a):
		a.pop()


	def getUserTweets(self, screen_name):
		api = self.api[0]
		# get a specific user's timeline
		tweets = api.GetUserTimeline(screen_name = screen_name, count = 200)
		# all_tweets = tweets[0].user.statuses_count
		if len(tweets) <= 0:
			return

		user_id = tweets[0].user.id

		
		file_obj = open('test/' + screen_name + '.txt','w')

		# while all_tweets > 0:
		while len(tweets) > 0:
			# length = len(tweets)
			# min < 1000000000000000000000
			for tt in tweets:
				# print (type(tt.id_str), type(tt.retweeted), type(tt.favorite_count), type(tt.created_at))
				# if tweets[-1].id < tt.id:
				# 	print 12345

				try:
					file_obj.write(tt.id_str + " " + tt.created_at + "\n")
					file_obj.write(tt.text.replace(u'\xa0', u' ').replace('\n','  ').encode("utf-8") + "\n")
				except:
					continue

			try:
				# RT @taylorswift13: So much love...(retweet)
				# tag #word  @user
				tweets = api.GetUserTimeline(screen_name = screen_name, count = 200, max_id = tweets[-1].id - 1)
			except:
				print screen_name + ": get timeline failed"
				return
			# all_tweets = all_tweets - length

		file_obj.close()

	def getUserTweetsRev(self, screen_name):
		api = self.api[0]
		# get a specific user's timeline
		tweets = api.GetUserTimeline(screen_name = screen_name, count = 2, )

		print tweets
		return
		# all_tweets = tweets[0].user.statuses_count
		if len(tweets) <= 0:
			return

		user_id = tweets[0].user.id

		
		file_obj = open('test/' + screen_name + '.txt','w')

		# while all_tweets > 0:
		while len(tweets) > 0:
			# length = len(tweets)
			for tt in tweets:
				# print (type(tt.id_str), type(tt.retweeted), type(tt.favorite_count), type(tt.created_at))
				try:
					file_obj.write(tt.text.replace(u'\xa0', u' ').replace('\n','  ').encode("utf-8") + "\n")
				except:
					continue

			try:
				# RT @taylorswift13: So much love...(retweet)
				# tag #word  @user
				tweets = api.GetUserTimeline(screen_name = screen_name, count = 200, max_id = tweets[-1].id - 1)
			except:
				print screen_name + ": get timeline failed"
				return
			# all_tweets = all_tweets - length

		file_obj.close()


	def getAllUsersTweets(self):
		sql = "select screenname from user" 
		try:
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
		except:
			return -1

		for ii in info:
			try:
				self.getUserTweets(ii[0])
				print ii[0] + " finished..."
			except:
				print ii[0] + " failed"
				continue
	


	def getFollowing(self, screen_name):
		file_obj = open('following/' + screen_name + '.txt','w')
		cursor = -1

		while cursor != 0:
			api = self.api[self.apiIndex]
			self.apiIndex = (self.apiIndex + 1) % self.apiCount
			out = api.GetFriendIDsPaged(screen_name = screen_name, cursor = cursor, count = 5000)
			cursor = out[0]
			friend_list = out[2]
			for fl in friend_list:
				file_obj.write(str(fl) + " ")
			file_obj.write("\n")

		file_obj.close()	
	
		
	def getFollowers(self, screen_name):
		file_obj = open('followers/' + screen_name + '.txt','w')
		cursor = -1
		
		while cursor != 0:
			api = self.api[self.apiIndex]
			self.apiIndex = (self.apiIndex + 1) % self.apiCount
			out = api.GetFollowerIDsPaged(screen_name = screen_name, cursor = cursor, count = 5000)
			cursor = out[0]
			friend_list = out[2]
			for fl in friend_list:
				file_obj.write(str(fl) + " ")
			file_obj.write("\n")

		file_obj.close()	


	def restart(self):
		sql = "select screenname from user" 
		try:
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
			for ii in info:
				self.bf.add(ii[0])
		except:
			return -1
		
		return

		
spider = Crawler()