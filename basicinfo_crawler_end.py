import time
import twitter
import config
import MySQLdb
import threading
from pybloom import BloomFilter

api_count = 58
api_list = []
user_list = []
extend_list = []
lock = threading.Lock()
bloom_filter = BloomFilter(capacity = 33000000, error_rate = 0.001)

class Crawler:
	def __init__(self):
		global api_list
		global api_count

		for i in range(api_count):
			api_list.append(twitter.Api(consumer_key = config.APP_INFO[i]['consumer_key'],
		                      consumer_secret = config.APP_INFO[i]['consumer_secret'],
		                      access_token_key = config.APP_INFO[i]['access_token_key'],
		                      access_token_secret = config.APP_INFO[i]['access_token_secret']))

	def bfs_user(self, root_users):
		i = 0
		threadPool = []
		threadNum = config.THREAD_NUM

		self.reload_users()
		self.extend_root_user(root_users[0 : 300])
		extendThread = ThreadExtend()
		extendThread.start()
		threadPool.append(extendThread)

		print 'extending ...'
		print 'sleeping ...' 
		time.sleep(6)

		while i < threadNum:
			crawThread = ThreadCrawler()
			crawThread.start()
			threadPool.append(crawThread)
			i = i + 1

		for thread in threadPool:
			thread.join()

	def reload_users(self):
		global bloom_filter
		print "reloading..."

		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		db.set_character_set('utf8')
		cursor = db.cursor()

		# for table_name in ['user_famous']:
		for table_name in ['user', 'user_1', 'user_all', 'user_bfs_relation', 'user_famous', 'user_random_3000']:
			sql = "select user_id from " + table_name
			try:
				cursor.execute(sql)
				user = cursor.fetchall()
				for user_id in user:
					bloom_filter.add(user_id[0])
			except Exception as e:
				print e

	def extend_root_user(self, root_users):
		global user_list, api_list, extend_list
		global bloom_filter, api_count

		print "extending root user..."

		api_index = 0
		sleep_count = 0

		for root_user in root_users:
			try:
				api_index = (api_index + 1) % api_count
				friends = api_list[api_index].GetFriendIDsPaged(user_id = root_user, cursor = -1, count = 200)
				friend_list = friends[2]
			except Exception as e:
				print e
				if hasattr(e, "message"):
					try:
						if e.message[0]['code'] == 88:
							print "sleeping..."
							time.sleep(900)
							continue
					except Exception as e2:
						print e2
						continue
				else:
					print e
				continue
		
			for fd in friend_list:
				if fd not in bloom_filter:
					bloom_filter.add(fd)
					user_list.append(fd)

		extend_list = user_list[0 : ]
				

class ThreadExtend(threading.Thread):
	def  __init__(self):
		threading.Thread.__init__(self)
		
	def run(self):
		global user_list, api_list, extend_list
		global bloom_filter, api_count
		
		count = 0
		api_index = 0
		sleep_count = 0

		while count < 30000000:
			user_id = extend_list.pop(0)
			try:
				api_index = (api_index + 1) % api_count
				friends = api_list[api_index].GetFriendIDsPaged(user_id = user_id, cursor = -1, count = 5000)
				friend_list = friends[2]
			except Exception as e:
				print e
				if hasattr(e, "message"):
					try:
						if e.message[0]['code'] == 88:
							print "sleeping..."
							time.sleep(900)
							continue
					except Exception as e2:
						print e2
						continue
				else:
					print e
				continue
		
			for fd in friend_list:
				try:
					if fd not in bloom_filter:
						count = count + 1
						bloom_filter.add(fd)
						extend_list.append(fd)
						if lock.acquire():
							user_list.append(fd)
							lock.release()
				except Exception as e:
					print e
					continue

			
class ThreadCrawler(threading.Thread):
	def  __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		global user_list, api_list
		global bloom_filter, api_count
	
		api_index = 0
		sleep_count = 0

		while len(user_list) > 0:
			if lock.acquire():
				user_id = user_list.pop(0)
				lock.release()
			print str(user_id) + " ..."
			
			db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
			db.set_character_set('utf8')
			cursor = db.cursor()

			try:
				api_index = (api_index + 1) % api_count
				user = api_list[api_index].GetUser(user_id = user_id)
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

				sql = """INSERT INTO user_random_3000(user_id, screen_name, name, location, created_at, description, statuses_count, friends_count, 
						followers_count, favourites_count, lang, protected, time_zone, verified, utc_offset, geo_enabled, listed_count,
						is_translator, default_profile_image, profile_background_color, profile_sidebar_fill_color, profile_image_url, crawler_date) VALUES
						('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s', %d, '%s', %d, '%s', %d, %d, %d, %d,
						'%s', '%s', '%s', '%s')""" % (user_id, user.screen_name, name, location, user.created_at, description, user.statuses_count, \
						user.friends_count, user.followers_count, user.favourites_count, user.lang, protected, user.time_zone, verified, \
						user.utc_offset, geo_enabled, listed_count, is_translator, default_profile_image, user.profile_background_color, \
						user.profile_sidebar_fill_color, user.profile_image_url, time.strftime('%Y-%m-%d',time.localtime(time.time()))) 

			except Exception as e:
				print e
				continue

			try:
				cursor.execute(sql)
				db.commit()
			except Exception as e:
				try:
					print sql
				except:
					continue
				print e
				continue
			db.close()
		

if __name__ == "__main__":
	db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
	db.set_character_set('utf8')
	cursor = db.cursor()

	sql = "select user_id from user_all_valid limit 355"
	try:
		cursor.execute(sql)
		user = cursor.fetchall()
	except Exception as e:
		print e

	crawler = Crawler()
	crawler.bfs_user(map(lambda x: x[0], user))

