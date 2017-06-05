import time
import twitter
import config
import MySQLdb
# import threading
# from pybloom import BloomFilter


class Crawler:
	def __init__(self):
		self.api_list = []

		for i in range(58):
			self.api_list.append(twitter.Api(consumer_key = config.APP_INFO[i]['consumer_key'],
		                      consumer_secret = config.APP_INFO[i]['consumer_secret'],
		                      access_token_key = config.APP_INFO[i]['access_token_key'],
		                      access_token_secret = config.APP_INFO[i]['access_token_secret']))

		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		db.set_character_set('utf8')
		cursor = db.cursor()
		self.db = db
		self.cursor = cursor

		sql = "select user_id from user_fill where protected = 0 and lang = 'en' and friends_count > 100 limit 100000, 50000"
		try:
			cursor.execute(sql)
			user = cursor.fetchall()
			self.user = map(lambda x: x[0], user)
		except Exception as e:
			print e

	def extend_user(self):
		api_index = 0
		sleep_count = 0
		api_count = 58
		api_list = self.api_list
		user = self.user
		cursor = self.cursor
		db = self.db

		while len(user) > 0:
			user_id = user.pop()

			try:
				api_index = (api_index + 1) % api_count
				friends = api_list[api_index].GetFriendIDsPaged(user_id = user_id, cursor = -1, count = 5000)
				friend_list = friends[2]
			except Exception as e:
				if hasattr(e, "message"):
					try:
						if e.message[0]['code'] == 88:
							sleep_count = sleep_count + 1
							if sleep_count == api_count:
								print "sleeping..."
								time.sleep(900)
								sleep_count = 0
							continue 
					except Exception as e2:
						print e2
						continue
				continue
		
			for fd in friend_list:
				
				sql = "select user_id from user_fill where user_id = '%s'" % fd
				try:
					u = None
					cursor.execute(sql)
					u = cursor.fetchall()
				except Exception as e:
					print e
					continue

				# print u
				# return

				if len(u) != 0:
					continue

				print fd
				sql = "insert into user_userid(user_id) values('%d')" % (fd)
				try:
					cursor.execute(sql)
					db.commit()
				except Exception as e:
					continue
					print e
			
		
if __name__ == "__main__":
	crawler = Crawler()
	crawler.extend_user()