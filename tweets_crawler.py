import twitter
import config
import MySQLdb
import time
import threading
from pymongo import MongoClient

# log_obj = open('log/log.txt','a')

class Crawler:
	def __init__(self):
		api = []

		for i in range(58):
			api.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))

		self.api = api

		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		cursor = db.cursor()
		self.cursor = cursor
		self.db = db


	def get_all_user_tweets(self):
		sql = "select user_id from user_5" 
		try:
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
		except:
			return -1

		i = 0
		threadNum = config.THREAD_NUM
		length = len(info)
		threadPool = []
		per_thread = length / threadNum
		
		while i < threadNum:
			if i + 1 == threadNum:
				crawThread = ThreadCrawler(info[i * per_thread : ], self.api)
			else:
				crawThread = ThreadCrawler(info[i * per_thread : (i + 1) * per_thread], self.api)
			
			crawThread.start()
			threadPool.append(crawThread)
			i = i + 1
			
		for thread in threadPool:
			thread.join()


	def restart(self):
		sql = "select userid from user" 
		try:
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
			for ii in info:
				return
				# self.bf.add(ii[0])
		except:
			return -1
		
		return


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

		for info in users:
			flag  = True
			tweets = [0]
			user_id = info[0]
			print user_id + " ..."
			
			while len(tweets) > 0:
				api_index = (api_index + 1) % api_count
				if flag:
					try:
						tweets = apis[api_index].GetUserTimeline(user_id = user_id, count = 200)
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
						tweets = apis[api_index].GetUserTimeline(user_id = user_id, count = 200, max_id = tweets[-1].id - 1)
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
					
				for tt in tweets:
					coordinates = None

					try:
						if tt.coordinates != None:
							coordinates = {
								"coordinates":tt.coordinates.coordinates,
								"type": tt.coordinates.type
							}
					except Exception as e:
						print e
						coordinates = None

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
						'id': tt.id_str, # String
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
					try:
						collect.insert_one(tweet)
					except Exception as e:
						print e
	
		

if __name__ == "__main__":
	crawler = Crawler()
	crawler.get_all_user_tweets()