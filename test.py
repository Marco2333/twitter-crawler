import twitter
import config
import MySQLdb
import time
from pymongo import MongoClient


class Crawler:
	def __init__(self):

		# print db.tweet
		# print db.collection_names()
		# for u in db.tweet.find():
  #  			print(u)
  # 		table.insert_one({'id':'1','name':'cnki'})

		# # db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		# # cursor = db.cursor()
		# # self.cursor = cursor
		# # self.db = db
		# return

		api = []
		self.apiCount = 17
		for i in range(self.apiCount):
			api.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))
		# for i in range(6000002, 6000010):
		# 	try:
		# 		info = api[2].GetUser(user_id = i)
		# 		print (info.id, info.screen_name)
		# 	except Exception as e:
		# 		print e
		# 		continue
		# return
		client = MongoClient('127.0.0.1', 27017)
		db_name = 'twitter'
		db = client[db_name]
		table = db['tweet']
		print table
		print 123

		# a = api[0].GetUser(user_id = 59)
		# print a
		# return 
		# a = [{'id':None}]
		# print a[-1]['id'] - 1
		# return
		a = [1,2,3,4,5,6,7]
		print a[0:]
		print a[1:3]
		
		u = api[0].GetUser(screen_name = 'to_mkl')
		print u
		return
		tweets = api[0].GetUserTimeline(screen_name = 'to_mkl', max_id = 0, count = 2)
		print tweets
		return
		print tweets[0]
		return

		self.api = api
		self.apiIndex = 0

		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		cursor = db.cursor()
		self.cursor = cursor
		self.db = db
		# self.getAllUsersTweets()
		self.getAllUsersRelation()
		# self.getFollowing('01secondstv')
		# out = self.api.GetFriendIDsPaged(screen_name = "mrmarcohan", cursor = -1, count = 100)
		# print out

	def getAllUsersRelation(self):
		sql = "select screenname, fansNum, watchNum from user" 
		try:
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
		except:
			return -1

		length = len(info) - 1

		while length >= 0:
			ii = info[length]
			length = length - 1
			try:
				if ii[2] < 50000:
					self.getFollowing(ii[0])
				if ii[1] < 100000:
					self.getFollowers(ii[0])
				print ii[0] + " finished..."
			except Exception as e:
				print ii[0] + " failed"
				
				if hasattr(e,"message"):
					print e.message
					try:
						if e.message[0]['code'] == 88:
							length = length + 1
							print "sleeping..."
							time.sleep(300)
					except:
						continue
				continue

	def getAllUsersTweets(self):
		sql = "select screenname from user" 
		try:
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
		except:
			return -1

		for ii in info:
			try:
				self.getUserTweets(ii[0])
				print ii[0] + " finished..."
			except:
				print ii[0] + " failed"
				continue
	

	def getUserTweets(self, screen_name):
		api = self.api
		# get a specific user's timeline
		tweets = api.GetUserTimeline(screen_name = screen_name, count = 200)
		# all_tweets = tweets[0].user.statuses_count
		if len(tweets) <= 0:
			return
		user_id = tweets[0].user.id

		sql = "update user set userid = '%s' where screenname = '%s'" % (user_id, screen_name)
		try:
		   self.cursor.execute(sql)
		   self.db.commit()
		except:
		   return -1

		# for s in tweets:
		# 	print s.id
		# return
		file_obj = open('tweets123/' + screen_name + '.txt','w')

		# while all_tweets > 0:
		while len(tweets) > 0:
			# length = len(tweets)
			for tt in tweets:
				# print (type(tt.id_str), type(tt.retweeted), type(tt.favorite_count), type(tt.created_at))
				try:
					file_obj.write(str(tt.id) + "\t" + str(tt.retweeted) + "\t" + str(tt.retweet_count) + "\t" + str(tt.favorite_count) + "\t" + tt.created_at.encode('utf-8') + "\n")
					file_obj.write(tt.text.replace(u'\xa0', u' ').replace('\n','  ').encode("utf-8") + "\n")
				except:
					continue

			try:
				# RT @taylorswift13: So much love...(retweet)
				# tag #word  @user
				tweets = api.GetUserTimeline(screen_name = screen_name, count = 200, max_id = tweets[-1].id - 1)
			except:
				print screen_name + ": get timeline failed"
				return
			# all_tweets = all_tweets - length

		file_obj.close()

	def getFollowing(self, screen_name):
		file_obj = open('following/' + screen_name + '.txt','w')
		cursor = -1

		while cursor != 0:
			api = self.api[self.apiIndex]
			self.apiIndex = (self.apiIndex + 1) % self.apiCount
			out = api.GetFriendIDsPaged(screen_name = screen_name, cursor = cursor, count = 5000)
			cursor = out[0]
			friend_list = out[2]
			for fl in friend_list:
				file_obj.write(str(fl) + " ")
			file_obj.write("\n")

		file_obj.close()	
	
		
	def getFollowers(self, screen_name):
		file_obj = open('followers/' + screen_name + '.txt','w')
		cursor = -1
		
		while cursor != 0:
			api = self.api[self.apiIndex]
			self.apiIndex = (self.apiIndex + 1) % self.apiCount
			out = api.GetFollowerIDsPaged(screen_name = screen_name, cursor = cursor, count = 5000)
			cursor = out[0]
			friend_list = out[2]
			for fl in friend_list:
				file_obj.write(str(fl) + " ")
			file_obj.write("\n")

		file_obj.close()	


	def restart(self):
		sql = "select screenname from user" 
		try:
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
			for ii in info:
				self.bf.add(ii[0])
		except:
			return -1
		
		return

		
spider = Crawler()