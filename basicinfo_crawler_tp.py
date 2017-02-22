import time
import twitter
import config
import MySQLdb
import threading

db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
db.set_character_set('utf8')
# db.ping(True)
cursor = db.cursor()



class Crawler:
	def __init__(self):
		api = []
		self.apiCount = 58
		for i in range(58):
			api.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))

		self.api = api


	def user_scan(self):
		i = 1
		j = 0
		index = 0
		threadPool = []
		api = self.api
		apiCount = self.apiCount
		threadNum = config.THREAD_NUM

		while i < 200:
			while j < threadNum:

				crawThread = ThreadCrawler(i, api[index])
				crawThread.start()
				threadPool.append(crawThread)

				index = (index + 1) % apiCount
				i = i + 1
				j = j + 1

			for thread in threadPool:
				thread.join()

			j = 0
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
		print user_id

	def run(self):
		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		db.set_character_set('utf8')
		cursor = db.cursor()

		user_id = self.user_id
		try:
			user = self.api.GetUser(user_id = user_id)
		except Exception as e:
			if hasattr(e, "message"):
				try:
					if e.message[0]['code'] == 88:
						print "sleeping..."
						time.sleep(10)
						return
					elif e.message[0]['code'] != 50:
						print e
						return
				except Exception as e2:
					print e2
					return
			else:
				print e
			return

		is_translator = 0
		if hasattr(user, "is_translator"):
			is_translator = 1 if user.is_translator else 0

		description = user.description.replace("'","\\'") if user.description else ''
		protected = 1 if user.protected else 0
		verified = 1 if user.verified else 0
		geo_enabled = 1 if user.geo_enabled else 0
		listed_count = user.listed_count if user.listed_count else 0
		default_profile_image = 1 if user.default_profile_image else 0 

		sql = """INSERT INTO user_1(user_id, screen_name, name, location, created_at, description, statuses_count, friends_count, 
				followers_count, favourites_count, lang, protected, time_zone, verified, utc_offset, geo_enabled, listed_count,
				is_translator, default_profile_image, profile_background_color, profile_sidebar_fill_color, crawler_date) VALUES
				('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s', %d, '%s', %d, '%s', %d, %d, %d, %d,
				'%s', '%s', '%s')""" % (user_id, user.screen_name, user.name, user.location, user.created_at, description, user.statuses_count, \
				user.friends_count, user.followers_count, user.favourites_count, user.lang, protected, user.time_zone, verified, \
				user.utc_offset, geo_enabled, listed_count, is_translator, default_profile_image, user.profile_background_color, \
				user.profile_sidebar_fill_color, time.strftime('%Y-%m-%d',time.localtime(time.time()))) 

		# global db
		# global cursor

		try:
			cursor.execute(sql)
			db.commit()
		except Exception as e:
			print e
			return -1
		db.close()

if __name__ == "__main__":
	crawler = Crawler()
	crawler.user_scan()

