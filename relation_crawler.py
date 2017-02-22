import twitter
import config
import MySQLdb
import time

class RelationshipCrawler:
	def __init__(self):
		api = []
		self.apiCount = 50
		for i in range(50):
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
		sql = "select userid, friends_count, followers_count from user" 
		try:
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
		except:
			return -1

		for ii in info:
			if ii[0] == '':
				continue
			try:
				# if ii[1] < 50000:
				# 	self.getFollowing(ii[0])
				if ii[2] < 100000:
					self.getFollowers(ii[0])
				print ii[0] + " finished..."
			except Exception as e:
				print ii[0] + " failed"
				print e
				continue


	def getFollowing(self, user_id):
		if len(user_id) <= 4:
			file_obj = open('following/other.txt','a')
			file_obj.write(":" + user_id)
			file_obj.write("\n")
		else:
			file_obj = open('following/' + user_id[0:4] + '.txt','a')
			file_obj.write(":" + user_id[4:])
			file_obj.write("\n")

		cursor = -1

		while cursor != 0:
			api = self.api[self.apiIndex]
			self.apiIndex = (self.apiIndex + 1) % self.apiCount
			
			try:
				out = api.GetFriendIDsPaged(user_id = user_id, cursor = cursor, count = 5000)
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
						file_obj.write("\n")
						file_obj.close()	
						return
				file_obj.write("\n")
				file_obj.close()			
				return

		file_obj.write("\n")
		file_obj.close()	
	
		
	def getFollowers(self, user_id):
		if len(user_id) <= 4:
			file_obj = open('followers/other.txt','a')
			file_obj.write(":" + user_id)
			file_obj.write("\n")
		else:
			file_obj = open('followers/' + user_id[0:4] + '.txt','a')
			file_obj.write(":" + user_id[4:])
			file_obj.write("\n")
		
		cursor = -1
		
		while cursor != 0:
			api = self.api[self.apiIndex]
			self.apiIndex = (self.apiIndex + 1) % self.apiCount

			try:
				out = api.GetFollowerIDsPaged(user_id = user_id, cursor = cursor, count = 5000)
				cursor = out[0]
				friend_list = out[2]
				for fl in friend_list:
					file_obj.write(str(fl) + " ")
			except Exception as e: 
				print e
				print user_id
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
						file_obj.write("\n")
						file_obj.close()	
						return
				file_obj.write("\n")
				file_obj.close()	
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

		
spider = RelationshipCrawler()