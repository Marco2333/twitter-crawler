import time
import twitter
import config
import MySQLdb
import threading
from pymongo import MongoClient

api_count = 5
api_list = []
api_index = 0
# user_list = []
# lock = threading.Lock()

class Crawler:
	def __init__(self):
		global api_list
		global api_count

		for i in range(api_count):
			api_list.append(twitter.Api(consumer_key = config.APP_INFO[i]['consumer_key'],
		                      consumer_secret = config.APP_INFO[i]['consumer_secret'],
		                      access_token_key = config.APP_INFO[i]['access_token_key'],
		                      access_token_secret = config.APP_INFO[i]['access_token_secret']))

	def fill_user_detail(self):
		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		db.set_character_set('utf8')
		cursor = db.cursor()

		# global user_list

		sql = "select screen_name from 100famous"

		try:
			cursor.execute(sql)
			user_list = cursor.fetchall()
			user_list = map(lambda x: x[0], user_list)
		except Exception as e:
			print e

		db.close()

		for screen_name in user_list:
			print screen_name
			# self.get_user_basicinfo(screen_name)
			self.get_tweet(screen_name)

		# i = 0
		# thread_pool = []
		# thread_num = config.THREAD_NUM

		# while i < thread_num:
		# 	craw_thread = ThreadCrawler()
		# 	craw_thread.start()
		# 	thread_pool.append(craw_thread)
		# 	i = i + 1

		# for thread in thread_pool:
		# 	thread.join()

	
	def get_user_basicinfo(self, screen_name):
		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		db.set_character_set('utf8')
		cursor = db.cursor()

		global api_count
		global api_index
		global api_list

		try:
			api_index = (api_index + 1) % api_count
			user = api_list[api_index].GetUser(screen_name = screen_name)
		except Exception as e:
			print e
			return

		try:
			is_translator = 0
			if hasattr(user, "is_translator"):
				is_translator = 1 if user.is_translator else 0

			name = user.name.replace("'","\\'")
			location = user.location.replace("'","\\'") if user.description else ''
			description = user.description.replace("'","\\'") if user.description else ''
			protected = 1 if user.protected else 0
			verified = 1 if user.verified else 0
			geo_enabled = 1 if user.geo_enabled else 0
			listed_count = user.listed_count if user.listed_count else 0
			default_profile_image = 1 if user.default_profile_image else 0 

			sql = """INSERT INTO user_fill_4(user_id, screen_name, name, location, created_at, description, statuses_count, friends_count, 
					followers_count, favourites_count, lang, protected, time_zone, verified, utc_offset, geo_enabled, listed_count,
					is_translator, default_profile_image, profile_background_color, profile_sidebar_fill_color, profile_image_url, crawler_date) VALUES
					('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s', %d, '%s', %d, '%s', %d, %d, %d, %d,
					'%s', '%s', '%s', '%s')""" % (user.id, user.screen_name, name, location, user.created_at, description, user.statuses_count, \
					user.friends_count, user.followers_count, user.favourites_count, user.lang, protected, user.time_zone, verified, \
					user.utc_offset, geo_enabled, listed_count, is_translator, default_profile_image, user.profile_background_color, \
					user.profile_sidebar_fill_color, user.profile_image_url, time.strftime('%Y-%m-%d',time.localtime(time.time()))) 

		except Exception as e:	
			print e
			return

		try:
			cursor.execute(sql)
			db.commit()
		except Exception as e:
			print e
			return
		
		db.close()


	def get_tweet(self, screen_name):
		client = MongoClient('127.0.0.1', 27017)
		db_name = 'twitter'
		db = client[db_name]
		collect = db['tweets']

		global api_count
		global api_index
		global api_list

		flag  = True
		tweets = [0]
		
		while len(tweets) > 0:
			api_index = (api_index + 1) % api_count
			if flag:
				try:
					tweets = api_list[api_index].GetUserTimeline(screen_name = screen_name, trim_user = True, count = 200)
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
									time.sleep(700)
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
					tweets = api_list[api_index].GetUserTimeline(screen_name = screen_name, count = 200, trim_user = True, max_id = tweets[-1].id - 1)
				except Exception as e:
					if hasattr(e, "message"):
						print e.message
						try:
							if e.message[0]['code'] == 88:
								sleep_count = sleep_count + 1
								if sleep_count == api_count:
									print "sleeping..."
									sleep_count = 0
									time.sleep(700)
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
		

		
if __name__ == "__main__":
	crawler = Crawler()
	crawler.fill_user_detail()
