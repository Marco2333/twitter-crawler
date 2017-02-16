import twitter
import config
import MySQLdb
import time

class Crawler:
	def __init__(self):
		api = []
		self.apiCount = 26
		for i in range(26):
			api.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))

		self.api = api
		self.apiIndex = 0
		self.sleep_count = 0
		
		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		cursor = db.cursor()
		self.cursor = cursor
		self.db = db
		
		self.getAllUsersRelation()


	def getAllUsersRelation(self):
		sql = "select screenname, fansNum, watchNum from user_1_1" 
		try:
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
		except:
			return -1

		for ii in info:
			if ii[0] == '':
				continue
			try:
				if ii[2] < 50000:
					self.getFollowing(ii[0])
				if ii[1] < 100000:
					self.getFollowers(ii[0])
				print ii[0] + " finished..."
			except Exception as e:
				print ii[0] + " failed"
				print e
				continue


	def getFollowing(self, screen_name):
		file_obj = open('following/' + screen_name + '.txt','w')
		cursor = -1

		while cursor != 0:
			api = self.api[self.apiIndex]
			self.apiIndex = (self.apiIndex + 1) % self.apiCount
			
			try:
				out = api.GetFriendIDsPaged(screen_name = screen_name, cursor = cursor, count = 5000)
				cursor = out[0]
				friend_list = out[2]
				for fl in friend_list:
					file_obj.write(str(fl) + " ")
			except Exception as e: 
				print e
				if hasattr(e,"message"):
					print e.message
					try:
						if e.message[0]['code'] == 88:
							self.sleep_count = self.sleep_count + 1
							if self.sleep_count == self.apiCount:
								print "sleeping..."
								time.sleep(900)
								self.sleep_count = 0
							continue
					except Exception as e2:
						print e2
						return
				return
			file_obj.write("\n")

		file_obj.close()	
	
		
	def getFollowers(self, screen_name):
		file_obj = open('followers/' + screen_name + '.txt','w')
		cursor = -1
		
		while cursor != 0:
			api = self.api[self.apiIndex]
			self.apiIndex = (self.apiIndex + 1) % self.apiCount

			try:
				out = api.GetFollowerIDsPaged(screen_name = screen_name, cursor = cursor, count = 5000)
				cursor = out[0]
				friend_list = out[2]
				for fl in friend_list:
					file_obj.write(str(fl) + " ")
			except Exception as e: 
				print e
				if hasattr(e,"message"):
					print e.message
					try:
						if e.message[0]['code'] == 88:
							self.sleep_count = self.sleep_count + 1
							if self.sleep_count == self.apiCount:
								print "sleeping..."
								time.sleep(900)
								self.sleep_count = 0
							continue
					except Exception as e2:
						print e2
						return
				return

			file_obj.write("\n")

		file_obj.close()	


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

		
spider = Crawler()