import twitter
import config
import MySQLdb
import time
from pybloom import BloomFilter

# import tweepy
# auth = tweepy.OAuthHandler('bRJ4nxfQ1lQpc0b9OiGyznwTP', 'duDNQlvxtYInexf8kBiSTUwAuaskty4iGd6HnPKfoWzLoSvJgc')
# auth.set_access_token('716652054446379008-4wz9tWCPDUa61FglUqrhk58zmJmtnP2', 'hNFCesJ2rADFcmIljjEmywxGcDc6HrV6ORGZqrqNDWLXF')
# api = tweepy.API(auth)
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print tweet.text

class Crawler:
	def __init__(self):
		api = []
		self.apiCount = 9
		for i in range(26):
			api.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))

		self.api = api
		self.apiIndex = 0

		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		cursor = db.cursor()
		self.cursor = cursor
		self.db = db
		self.sleep_count = 0
		self.bf = BloomFilter(capacity = 5000000, error_rate = 0.001)
		self.bf.add(config.INITIAL_USER)
		self.userList = [config.INITIAL_USER]
		# self.getAllUsersTweets()
		# self.getAllUsersRelation()
		# self.getFollowing('01secondstv')
		# a = api[5].GetUser(screen_name = 'kobebryant')
		# print a 
		# return
		# while True:
		# 	n = n + 1
		# 	try:
		# 		print n
		# 		tweets = api.GetUserTimeline(screen_name = 'mrmarcohan', count = 2)
		# 		for tt in tweets:
		# 			print tt
		# 		# friends = api.GetFriendsPaged(screen_name = 'mrmarcohan', cursor = -1, count = 1)
		# 		# print friends
		# 	except Exception as e:
		# 		print e
		# 		print n
		# 		return
		# self.restart()
		# self.getUsersIDByFollowing()
		# self.getFollowing('mrmarcohan')
		self.sleep_count = 0
		self.getAllUsersRelation()

	def getUsersIDByFollowing(self):
		print "starting..."
		sleep_count = 0
		count = 0
		sql = "INSERT INTO user_1(userid) VALUES ('"
		while True:
			count = count + 1
			if count > 5000000:
				return

			user_id = self.userList.pop()
			api = self.api[self.apiIndex]
			self.apiIndex = (self.apiIndex + 1) % self.apiCount
			try:
				out = api.GetFriendIDsPaged(user_id = user_id, cursor = -1, count = 5000)
			except Exception as e:
				print e
				if hasattr(e,"message"):
					print e.message
					try:
						if e.message[0]['code'] == 88:
							sleep_count = sleep_count + 1
							if sleep_count == self.apiCount:
								print "sleeping..."
								time.sleep(900)
								sleep_count = 0
							continue
					except Exception as e1:
						print e1
						continue
				continue

			for id in out[2]:
				if id not in self.bf:
					self.bf.add(id)
					self.userList.append(id)
					try:
						self.cursor.execute(sql + str(id) + "')")
						self.db.commit()
					except Exception as e:
						print e


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

		# length = len(info) - 1

		# while length >= 0:
		# 	ii = info[length]
		# 	length = length - 1
		# 	try:
		# 		if ii[2] < 50000:
		# 			self.getFollowing(ii[0])
		# 		if ii[1] < 100000:
		# 			self.getFollowers(ii[0])
		# 		print ii[0] + " finished..."
		# 	except Exception as e:
		# 		print ii[0] + " failed"
				
		# 		if hasattr(e,"message"):
		# 			print e.message
		# 			try:
		# 				if e.message[0]['code'] == 88:
		# 					length = length + 1
		# 					print "sleeping..."
		# 					time.sleep(300)
		# 			except:
		# 				continue
		# 		continue


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
						continue
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
						continue
				return

			file_obj.write("\n")

		file_obj.close()	

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