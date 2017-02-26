import time
import twitter
import config
import MySQLdb
import threading




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
		i = 0
		total = 4000000
		id_count = 2000000
		threadPool = []
		threadNum = config.THREAD_NUM
		per_thread = id_count / threadNum

		while i < threadNum:
			if i + 1 == threadNum:
				crawThread = ThreadCrawler(i * per_thread + 2000001, total, self.api)
			else:
				crawThread = ThreadCrawler(i * per_thread + 2000001, (i + 1) * per_thread + 2000000, self.api)
			crawThread.start()
			threadPool.append(crawThread)
			i = i + 1

		for thread in threadPool:
			thread.join()

	def restart(self):
		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		db.set_character_set('utf8')
		# db.ping(True)
		cursor = db.cursor()

		sql = "select user_id from user_5" 
		try:
			cursor.execute(sql)
			info = cursor.fetchall()
			# for ii in info:
			# 	self.bf.add(ii[0])
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
		# sleep_count = 0

		for info in users:
			user_id = info[0]
			print user_id + " ..."
			
			db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
			db.set_character_set('utf8')
			cursor = db.cursor()

			sql = "delete from user_5 where user_id = '%s'" % (user_id) 
			try:
				cursor.execute(sql)
				db.commit()
			except Exception as e:
				print e
				continue

			try:
				api_index = (api_index + 1) % api_count
				user = apis[api_index].GetUser(user_id = user_id)
			except Exception as e:
				if hasattr(e, "message"):
					try:
						if e.message[0]['code'] == 88:
							print "sleeping..."
							time.sleep(60)
							continue
						elif e.message[0]['code'] != 50:
							print e
							continue
					except Exception as e2:
						print e2
						continue
				else:
					print e
				continue

			is_translator = 0
			if hasattr(user, "is_translator"):
				is_translator = 1 if user.is_translator else 0

			description = user.description.replace("'","\\'") if user.description else ''
			protected = 1 if user.protected else 0
			verified = 1 if user.verified else 0
			geo_enabled = 1 if user.geo_enabled else 0
			listed_count = user.listed_count if user.listed_count else 0
			default_profile_image = 1 if user.default_profile_image else 0 

			sql = """INSERT INTO user_5(user_id, screen_name, name, location, created_at, description, statuses_count, friends_count, 
					followers_count, favourites_count, lang, protected, time_zone, verified, utc_offset, geo_enabled, listed_count,
					is_translator, default_profile_image, profile_background_color, profile_sidebar_fill_color, profile_image_url, crawler_date) VALUES
					('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s', %d, '%s', %d, '%s', %d, %d, %d, %d,
					'%s', '%s', '%s', '%s')""" % (user_id, user.screen_name, user.name, user.location, user.created_at, description, user.statuses_count, \
					user.friends_count, user.followers_count, user.favourites_count, user.lang, protected, user.time_zone, verified, \
					user.utc_offset, geo_enabled, listed_count, is_translator, default_profile_image, user.profile_background_color, \
					user.profile_sidebar_fill_color, user.profile_image_url, time.strftime('%Y-%m-%d',time.localtime(time.time()))) 

			try:
				cursor.execute(sql)
				db.commit()
			except Exception as e:
				print e
				continue
			db.close()



# class ThreadCrawler(threading.Thread):
# 	def  __init__(self, lower_bound, upper_bound, api):
# 		threading.Thread.__init__(self)
# 		self.lower_bound = lower_bound
# 		self.upper_bound = upper_bound
# 		self.api = api
		

# 	def run(self):
# 		user_id = self.lower_bound - 1
# 		upper_bound = self.upper_bound
# 		apis = self.api
# 		api_count = 58
# 		api_index = 0

# 		# global db
# 		# global cursor

# 		while user_id < upper_bound:
# 			print str(user_id) + " ..."
# 			db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
# 			db.set_character_set('utf8')
# 			cursor = db.cursor()
# 			try:
# 				user_id = user_id + 1
# 				api_index = (api_index + 1) % api_count
# 				user = apis[api_index].GetUser(user_id = user_id)

# 			except Exception as e:
# 				if hasattr(e, "message"):
# 					try:
# 						if e.message[0]['code'] == 88:
# 							print "sleeping..."
# 							time.sleep(60)
# 							user_id = user_id - 1
# 							continue
# 						elif e.message[0]['code'] != 50:
# 							print e
# 							continue
# 					except Exception as e2:
# 						print e2
# 						continue
# 				else:
# 					print e
# 				continue

# 			is_translator = 0
# 			if hasattr(user, "is_translator"):
# 				is_translator = 1 if user.is_translator else 0

# 			description = user.description.replace("'","\\'") if user.description else ''
# 			protected = 1 if user.protected else 0
# 			verified = 1 if user.verified else 0
# 			geo_enabled = 1 if user.geo_enabled else 0
# 			listed_count = user.listed_count if user.listed_count else 0
# 			default_profile_image = 1 if user.default_profile_image else 0 

# 			sql = """INSERT INTO user_2(user_id, screen_name, name, location, created_at, description, statuses_count, friends_count, 
# 					followers_count, favourites_count, lang, protected, time_zone, verified, utc_offset, geo_enabled, listed_count,
# 					is_translator, default_profile_image, profile_background_color, profile_sidebar_fill_color, profile_image_url, crawler_date) VALUES
# 					('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s', %d, '%s', %d, '%s', %d, %d, %d, %d,
# 					'%s', '%s', '%s', '%s')""" % (user_id, user.screen_name, user.name, user.location, user.created_at, description, user.statuses_count, \
# 					user.friends_count, user.followers_count, user.favourites_count, user.lang, protected, user.time_zone, verified, \
# 					user.utc_offset, geo_enabled, listed_count, is_translator, default_profile_image, user.profile_background_color, \
# 					user.profile_sidebar_fill_color, user.profile_image_url, time.strftime('%Y-%m-%d',time.localtime(time.time()))) 

# 			try:
# 				cursor.execute(sql)
# 				db.commit()
# 			except Exception as e:
# 				print e
# 				continue
# 			db.close()

			

if __name__ == "__main__":
	crawler = Crawler()
	# crawler.user_scan()
	crawler.restart()
