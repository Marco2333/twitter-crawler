import twitter
import config
import MySQLdb
import time
import threading

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
		sql = "select user_id from user" 
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
				self.bf.add(ii[0])
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
		# global log_obj
		api_index = 0
		api_count = 58
		sleep_count = 0

		for info in users:

			user_id = info[0]
			print user_id + " ..."

			try: 
				tweets = apis[api_index].GetUserTimeline(user_id = user_id, count = 200)
			except Exception as e:
				print e

			if len(tweets) == 0:
				continue

			file_obj = open('tweets/' + user_id + '.txt','w')

			for tt in tweets:
				# insert into mongodb
				try:
					# file_obj.write(str(tt.id) + "\t" + str(tt.retweet_count) + "\t" + str(tt.favorite_count) + "\t" + tt.created_at.encode('utf-8') + "\n")
					file_obj.write(tt.text.replace(u'\xa0', u' ').replace('\n','  ').encode("utf-8") + "\n")
				except Exception as e1:
					print e1
					break
			
			while len(tweets) > 0:
				try:
					# RT @taylorswift13: So much love...(retweet)  # tag #word  @user
					api_index = (api_index + 1) % api_count
					tweets = apis[api_index].GetUserTimeline(user_id = user_id, count = 200, max_id = tweets[-1].id - 1)
				except Exception as e:
					print e
					break
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
								# log_obj.write(user_id + " " + time.strftime('%Y-%m-%d',time.localtime(time.time())) + "\n")
								# log_obj.write(e.message[0]['message'])
						except Exception as e2:
							print e2
							break
					else:
						print e
						break
					
				for tt in tweets:
					# insert into mongodb
					try:
						# file_obj.write(str(tt.id) + "\t" + str(tt.retweet_count) + "\t" + str(tt.favorite_count) + "\t" + tt.created_at.encode('utf-8') + "\n")
						file_obj.write(tt.text.replace(u'\xa0', u' ').replace('\n','  ').encode("utf-8") + "\n")
					except Exception as e1:
						print e1
						break
			file_obj.close()
	

		

if __name__ == "__main__":
	crawler = Crawler()
	crawler.get_all_user_tweets()