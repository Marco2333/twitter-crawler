import twitter
import config
# import MySQLdb
import time
import threading


class Crawler:
	def __init__(self):
		api = []
		for i in range(35):
			api.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))

		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		cursor = db.cursor()
		self.cursor = cursor
		self.db = db
		self.api = api


	def user_scan(self):
		i = 0
		index = 0
		threadPool = []
		threadNum = config.THREAD_NUM

		while i < 1000000:
			while i < threadNum:
				crawThread = ThreadCrawler(i, api[index])
				crawThread.start()
				treadPool.append(crawThread)
				index = (index + 1) % apiCount
				i = i + 1

			for thread in threadPool:
				thread.join()

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
		try:
			user = self.api.GetUser(user_id = self.user_id)
		except Exception as e:
			print e
			if hasattr(e, "message"):
					print e.message
					try:
						if e.message[0]['code'] == 88:
								print "sleeping..."
								time.sleep(100)
							continue
					except Exception as e2:
						print e2
						return
				return

		protected = 1 if user.protected else 0 
		verified = 1 if user.verified else 0 
		geo_enabled = 1 if user.geo_enabled else 0 
		is_translator = 1 if user.is_translator else 0 
		default_profile_image = 1 if user.default_profile_image else 0 

		sql = """INSERT INTO user_1(user_id, screen_name, name, location, created_at, description, statuses_count, friends_count, 
				followers_count, favourites_count, lang, protected, time_zone, verified, utc_offset, geo_enabled, listed_count,
				is_translator, default_profile_image, profile_background_color, profile_sidebar_fill_color, crawler_date) VALUES 
				('%s', '%s', '%s', '%s', '%s', '%s', '%d', '%d', '%d', '%d', '%s', '%d', '%s', '%d', '%d', '%d', '%d', '%d', '%d', 
				'%s', '%s', '%s')""" % (user_id, user.screen_name, user.name, user.location, user.created_at, user.description, user.statuses_count, \
				user.friends_count, user.followers_count, user.favourites_count, user.lang, protected, user.time_zone, verified, \
				user.utc_offset, geo_enabled, user.listed_count, is_translator, default_profile_image, user.profile_background_color, \
				user.profile_sidebar_fill_color, time.strftime('%Y-%m-%d',time.localtime(time.time()))) 

		try:
			# 执行sql语句
			self.cursor.execute(sql)
			# 提交到数据库执行
			self.db.commit()
		except:
		   return -1

if __name__ == "__main__":
	crawler = Crawler()
	crawler.user_scan()

