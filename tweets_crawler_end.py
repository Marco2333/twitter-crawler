import twitter
import config
import MySQLdb
import time
import threading
from pymongo import MongoClient

LOCK = threading.Lock()

class Crawler:
	def __init__(self):
		apis = []

		for i in range(58):
			apis.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))

		self.apis = apis

		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		cursor = db.cursor()
		self.cursor = cursor
		self.db = db


	def get_all_user_tweets(self):
		sql = "select user_id from user_famous" 
		try:
			self.cursor.execute(sql)
			user_info = self.cursor.fetchall()
		except:
			return -1

		i = 0
		thread_pool = []
		thread_num = config.THREAD_NUM
		user_info = list(user_info)

		while i < thread_num:
			craw_thread = ThreadCrawler(user_info, self.apis)
			craw_thread.start()
			thread_pool.append(craw_thread)
			i = i + 1

		for thread in thread_pool:
			thread.join()


class ThreadCrawler(threading.Thread):
	def  __init__(self, users, apis):
		threading.Thread.__init__(self)
		self.users = users
		self.apis = apis
		

	def run(self):
		apis = self.apis
		users = self.users
		
		api_index = 0
		api_count = 58
		sleep_count = 0

		client = MongoClient('127.0.0.1', 27017)
		db_name = 'twitter'
		db = client[db_name]
		collect = db['tweets_2']

		while len(users) > 0:
			if LOCK.acquire():
				user_id = users.pop(0)
				LOCK.release()
				
			user_id = user_id[0]

			print str(user_id) + " ..."

			flag  = True
			tweets = [0]
			
			while len(tweets) > 0:
				api_index = (api_index + 1) % api_count
				if flag:
					try:
						tweets = apis[api_index].GetUserTimeline(user_id = user_id, trim_user = True, count = 200)
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
						tweets = apis[api_index].GetUserTimeline(user_id = user_id, count = 200, trim_user = True, max_id = tweets[-1].id - 1)
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
	crawler.get_all_user_tweets()