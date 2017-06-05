import time
import twitter
import config
import MySQLdb
import threading
import warnings

warnings.filterwarnings("ignore")

api_count = 58
api_list = []
user_list = []
lock = threading.Lock()

class Crawler:
	def __init__(self):
		global api_list
		global api_count

		for i in range(api_count):
			api_list.append(twitter.Api(consumer_key = config.APP_INFO[i]['consumer_key'],
		                      consumer_secret = config.APP_INFO[i]['consumer_secret'],
		                      access_token_key = config.APP_INFO[i]['access_token_key'],
		                      access_token_secret = config.APP_INFO[i]['access_token_secret']))

	def restart(self):
		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		db.set_character_set('utf8')
		cursor = db.cursor()

		i = 2

		sql = "insert into user_fill select * from user_fill_%s" % i
		cursor.execute(sql)
		db.commit()
		
		sql = "delete from user_userid_%s where user_id in (select user_id from user_fill_%s)" % (i, i)
		cursor.execute(sql)
		db.commit()
		
		sql = "delete from user_fill_%s" % i
		cursor.execute(sql)
		db.commit()

		db.close()
				

	def fill_user_detail(self):
		n = 0
		while n < 4:
			n += 1
			print str(n) + ' ...'
			db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
			db.set_character_set('utf8')
			cursor = db.cursor()

			global user_list

			sql = "select user_id from user_userid_2 limit 300000"

			try:
				cursor.execute(sql)
				user_list = cursor.fetchall()
				user_list = map(lambda x: x[0], user_list)
			except Exception as e:
				print e

			i = 0
			thread_pool = []
			thread_num = config.THREAD_NUM

			while i < thread_num:
				craw_thread = ThreadCrawler()
				craw_thread.start()
				thread_pool.append(craw_thread)
				i = i + 1

			for thread in thread_pool:
				thread.join()

			cursor.close()
			db.close()
			self.restart()

		
class ThreadCrawler(threading.Thread):
	def  __init__(self):
		threading.Thread.__init__(self)
		print 'thread start ...'

	def run(self):
		global user_list, api_list
		global api_count
	
		api_index = 0
		sleep_count = 0

		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		db.set_character_set('utf8')
		cursor = db.cursor()

		while len(user_list) > 0:
			if lock.acquire():
				user_id = user_list.pop(0)
				lock.release()
			# print str(user_id) + " ..."
			
			try:
				api_index = (api_index + 1) % api_count
				user = api_list[api_index].GetUser(user_id = user_id)
			except Exception as e:
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

				sql = """INSERT INTO user_fill_2(user_id, screen_name, name, location, created_at, description, statuses_count, friends_count, 
						followers_count, favourites_count, lang, protected, time_zone, verified, utc_offset, geo_enabled, listed_count,
						is_translator, default_profile_image, profile_background_color, profile_sidebar_fill_color, profile_image_url, crawler_date) VALUES
						('%s', '%s', '%s', '%s', '%s', '%s', %d, %d, %d, %d, '%s', %d, '%s', %d, '%s', %d, %d, %d, %d,
						'%s', '%s', '%s', '%s')""" % (user_id, user.screen_name, name, location, user.created_at, description, user.statuses_count, \
						user.friends_count, user.followers_count, user.favourites_count, user.lang, protected, user.time_zone, verified, \
						user.utc_offset, geo_enabled, listed_count, is_translator, default_profile_image, user.profile_background_color, \
						user.profile_sidebar_fill_color, user.profile_image_url, time.strftime('%Y-%m-%d',time.localtime(time.time()))) 

			except Exception as e:	
				continue

			try:
				cursor.execute(sql)
				db.commit()
			except Exception as e:
				continue
		
		db.close()

if __name__ == "__main__":
	crawler = Crawler()
	crawler.fill_user_detail()