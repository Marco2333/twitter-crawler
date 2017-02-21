import twitter
import config
# import MySQLdb
import time
import threading

log_obj = open('log/log.txt','a')
temp_api = []

class Crawler:
	def __init__(self):
		global temp_api
		api = []
		self.apiCount = 35
		for i in range(35):
			api.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))

		for i in range(-10):
			temp_api.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))

		self.api = api

		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		cursor = db.cursor()
		self.cursor = cursor
		self.db = db


	def get_all_user_tweets(self):
		sql = "select userid from user" 
		try:
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
		except:
			return -1

		i = 0
		index = 0
		threadNum = config.THREAD_NUM
		length = len(info)
		api = self.api
		apiCount = self.apiCount
		threadPool = []
		while True:
			while i < threadNum:
				crawThread = ThreadCrawler(info.pop(0)[0], api[index])
				crawThread.start()
				treadPool.append(crawThread)
				index = (index + 1) % apiCount
				i = i + 1
				if i >= length:
					break

			for thread in threadPool:
				thread.join()

			if i >= length:
				print "finished..."
				return

			threadPool = []


	def restart(self):
		sql = "select userid from user" 
		try:
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
			for ii in info:
				self.bf.add(ii[0])
		except:
			return -1
		
		return


class ThreadCrawler(threading.Thread):
	def  __init__(self, user_id, api):
		threading.Thread.__init__(self)
		self.user_id = user_id
		self.api = api

	def run(self):
		file_obj = open('tweets/' + user_id + '.txt','w')
		tweets = [{'id':0}]
		api = self.api

		global log_obj
		global temp_api
		temp_count = 0

		while len(tweets) > 0:
			try:
				# RT @taylorswift13: So much love...(retweet)  # tag #word  @user
				tweets = api.GetUserTimeline(user_id = user_id, count = 200, max_id = tweets[-1]['id'] - 1)
			except Exception as e:
				print e
				if hasattr(e, "message"):
					print e.message
					try:
						if e.message[0]['code'] == 88:
							api = temp_api[temp_count]
							temp_count = temp_count + 1

							if temp_count == 8:
								print "sleeping..."
								temp_count = 0
								time.sleep(900)
							continue
						else:
							log_obj.write(user_id + " " + time.strftime('%Y-%m-%d',time.localtime(time.time())) + "\n")
							log_obj.write(e.message[0]['message'])
					except Exception as e2:
						print e2
						continue
				return
				
			for tt in tweets:
				# insert into mongodb
				try:
					file_obj.write(str(tt.id) + "\t" + str(tt.retweet_count) + "\t" + str(tt.favorite_count) + "\t" + tt.created_at.encode('utf-8') + "\n")
					file_obj.write(tt.text.replace(u'\xa0', u' ').replace('\n','  ').encode("utf-8") + "\n")
				except Exception as e1:
					print e1
					continue

		file_obj.close()
		
		description = user.description.replace("'","\\'") if user.description else ''
		protected = 1 if user.protected else 0
		verified = 1 if user.verified else 0
		geo_enabled = 1 if user.geo_enabled else 0
		default_profile_image = 1 if user.default_profile_image else 0 

		

if __name__ == "__main__":
	crawler = Crawler()
	crawler.get_all_user_tweets()

