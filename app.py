import twitter
import config
import MySQLdb

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
		for i in range(11):
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

		for ii in info:
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
			# return

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
			self.apiIndex = (self.apiIndex + 1) % 11
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
			self.apiIndex = (self.apiIndex + 1) % 11
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
			# 执行sql语句
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
			for ii in info:
				self.bf.add(ii[0])
		except:
			return -1
		
		return

		
spider = Crawler()