import twitter
import config
import MySQLdb
import time
from pymongo import MongoClient


class Crawler:
	def __init__(self):
		api = []
		self.apiCount = 58
		for i in range(self.apiCount):
			api.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))
		self.api = api
		
		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		cursor = db.cursor()
		self.cursor = cursor
		self.db = db

	def get_basic_info(self, screen_name):
		user = self.api[0].GetUser(screen_name = screen_name)

		is_translator = 0
		if hasattr(user, "is_translator"):
			is_translator = 1 if user.is_translator else 0

		description = user.description.replace("'","\\'") if user.description else ''
		protected = 1 if user.protected else 0
		verified = 1 if user.verified else 0
		geo_enabled = 1 if user.geo_enabled else 0
		listed_count = user.listed_count if user.listed_count else 0
		default_profile_image = 1 if user.default_profile_image else 0 

		sql = """INSERT INTO user_total(user_id, screen_name, name, location, created_at, description, statuses_count, friends_count, 
				followers_count, favourites_count, lang, protected, time_zone, verified, utc_offset, geo_enabled, listed_count,
				is_translator, default_profile_image, profile_background_color, profile_sidebar_fill_color, profile_image_url, crawler_date) VALUES
				('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s', %d, '%s', %d, '%s', %d, %d, %d, %d,
				'%s', '%s', '%s', '%s')""" % (user.id, screen_name, user.name, user.location, user.created_at, description, user.statuses_count, \
				user.friends_count, user.followers_count, user.favourites_count, user.lang, protected, user.time_zone, verified, \
				user.utc_offset, geo_enabled, listed_count, is_translator, default_profile_image, user.profile_background_color, \
				user.profile_sidebar_fill_color, user.profile_image_url, time.strftime('%Y-%m-%d',time.localtime(time.time()))) 

		try:
			self.cursor.execute(sql)
			self.db.commit()
		except Exception as e:
			print e

	def get_following(self, screen_name):
		file_obj = open('following_user/' + screen_name + '.txt','w')

		apis = self.api
		api_index = 0
		api_count = self.apiCount
		sleep_count = 0

		cursor = -1

		while cursor != 0:
			api = apis[api_index]
			api_index = (api_index + 1) % api_count
			try:
				out = api.GetFriendIDsPaged(screen_name = screen_name, cursor = cursor, count = 5000)
			except Exception as e:
				if hasattr(e, "message"):
					print e.message
					try:
						if e.message[0]['code'] == 88:
							sleep_count = sleep_count + 1
							if sleep_count == api_count:
								print "sleeping..."
								sleep_count = 0
								time.sleep(900)
							continue
						else:
							print e
							break
					except Exception as e2:
						print e2
						break
				else:
					print e
					break

			cursor = out[0]
			friend_list = out[2]
			for fl in friend_list:
				file_obj.write(str(fl) + " ")
			file_obj.write("\n")

		file_obj.close()


	def get_followers(self, screen_name):
		file_obj = open('followers_user/' + screen_name + '.txt','w')

		apis = self.api
		api_index = 20
		api_count = self.apiCount
		sleep_count = 0
		cursor = -1

		while cursor != 0:
			api = apis[api_index]
			api_index = (api_index + 1) % api_count
			try:
				out = api.GetFollowerIDsPaged(screen_name = screen_name, cursor = cursor, count = 5000)
			except Exception as e:
				if hasattr(e, "message"):
					print e.message
					try:
						if e.message[0]['code'] == 88:
							sleep_count = sleep_count + 1
							if sleep_count == api_count:
								print "sleeping..."
								sleep_count = 0
								time.sleep(900)
							continue
						else:
							print e
							break
					except Exception as e2:
						print e2
						break
				else:
					print e
					break

			cursor = out[0]
			friend_list = out[2]
			for fl in friend_list:
				file_obj.write(str(fl) + " ")
			file_obj.write("\n")

		file_obj.close()	


	def get_user_tweets(self, screen_name):
		apis = self.api
		api_index = 0
		api_count = self.apiCount
		flag = True
		tweets = [0]
		sleep_count = 0

		# file_obj = open('tweets_user/' + screen_name + '.txt','w')
		client = MongoClient('127.0.0.1', 27017)
		db_name = 'twitter'
		db = client[db_name]
		collect = db['tweets_famous']

		while len(tweets) > 0:
			api_index = (api_index + 1) % api_count
			if flag:
				try:
					tweets = apis[api_index].GetUserTimeline(screen_name = screen_name, count = 200)
					flag = False
				except Exception as e:
					if hasattr(e, "message"):
						print e.message
						try:
							if e.message[0]['code'] == 88:
								sleep_count = sleep_count + 1
								if sleep_count == api_count:
									print "sleeping..."
									sleep_count = 0
									time.sleep(800)
								flag = True
								continue
							else:
								print e
								break
						except Exception as e2:
							print e2
							break
					else:
						print e
						break
			else:
				try:
					# RT @taylorswift13: So much love...(retweet)  # tag #word  @user
					tweets = apis[api_index].GetUserTimeline(screen_name = screen_name, count = 200, max_id = tweets[-1].id - 1)
				except Exception as e:
					if hasattr(e, "message"):
						print e.message
						try:
							if e.message[0]['code'] == 88:
								sleep_count = sleep_count + 1
								if sleep_count == api_count:
									print "sleeping..."
									sleep_count = 0
									time.sleep(800)
								continue
							else:
								print e
								break
						except Exception as e2:
							print e2
							break
					else:
						print e
						break
				
			# for tt in tweets:
			# 	try:
			# 		file_obj.write(tt.text.replace(u'\xa0', u' ').replace('\n','  ').encode("utf-8") + "\n")
			# 	except Exception as e1:
			# 		print e1
			# 		continue
			for tt in tweets:
				tweet = {
					# 'contributors': tt.,
					'coordinates': tt.coordinates,  # Coordinates
					'created_at': tt.created_at, # String
					# 'current_user_retweet': None,
					'favorite_count': tt.favorite_count, # int
					# 'favorited': tt.favorited,
					'filter_level': tt.filter_level if hasattr(tt, 'filter_level') else '', # String
					# 'geo': tt.geo,
					'hashtags': map(lambda x: x.text, tt.hashtags), # {'0': ,'1':}
					'_id': tt.id_str, # String
					# 'id_str': tt.id_str,
					'in_reply_to_screen_name': tt.in_reply_to_screen_name,
					'in_reply_to_status_id': tt.in_reply_to_status_id,
					'in_reply_to_user_id': tt.in_reply_to_user_id,
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
				try:
					collect.insert_one(tweet)
				except Exception as e:
					print e

		# file_obj.close()

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

		
if __name__ == "__main__":
	name_list = ['floydmayweather', 'jp_books', 'robertdowneyjr', 'cristiano', 'd_copperfield', 
				'ryanseacrest', 'jldaily', 'kobebryant', 'leodicaprio', 'jimmybuffett', 'srbachchan', 
				'tim_cook', 'barackobama', 'hillaryclinton', 'theterminal']

	crawler = Crawler()

	for user in name_list:
		crawler.get_user_tweets(user)
	# crawler.get_followers('barackobama')


