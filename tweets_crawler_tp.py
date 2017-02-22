import twitter
import config
import MySQLdb
import time

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
		# self.apiIndex = 0
		# self.months = dict(Jan = '1', Feb = '2', Mar = '3', Apr = '4', \
		# 				May = '5', Jun = '6', Jul = '7', Aug = '8', \
		# 				Sep = '9', Oct = '10', Nov = '11', Dec = '12')

		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		cursor = db.cursor()
		self.cursor = cursor
		self.db = db
		# self.sleep_count = 0
		self.getAllUsersTweets()
		# self.getUserTweets('17919972')
		# print api[0].GetUser(screen_name='mrmarcohan')


	def getAllUsersTweets(self):
		sql = "select user_id from user_5" 
		try:
			self.cursor.execute(sql)
			info = self.cursor.fetchall()
		except:
			return -1

		for ii in info:
			try:
				self.getUserTweets(ii[0])
				print ii[0] + " finished..."
			except Exception as e:
				print ii[0] + " failed"
				print e
				continue
	

	def getUserTweets(self, user_id):
		api = self.api[self.apiIndex]
		self.apiIndex = (self.apiIndex + 1) % self.apiCount
		try:
			# get a specific user's timeline
			tweets = api.GetUserTimeline(user_id = user_id, count = 200)
		except Exception as e:
			print str(user_id) + ": get timeline failed"
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
							self.getUserTweets(user_id)
							return
						
				except Exception as e2:
					print e2
			return

		if len(tweets) <= 0:
			return

		user = tweets[0].user
		screen_name = user.screen_name
		join_date = user.created_at
		print screen_name + "...."
		try:
			jd = join_date.split(' ')
			join_date = jd[5] + "-" + self.months[jd[1]] + "-" + jd[2]
		except Exception as e:
			print e
			join_date = ""

		# all_tweets = tweets[0].user.statuses_count

		sql = """update user_1_2 set screenname = '%s', name = '%s', location = '%s', joinDate = '%s', bio = '%s', 
				tweetNum = '%s', watchNum = '%s', fansNum = '%s', likeNum = '%s', created_at = '%s' where userid = '%s'""" \
				% (screen_name, user.name, user.location, join_date, user.description, user.statuses_count, \
				user.friends_count, user.followers_count, user.favourites_count, time.strftime('%Y-%m-%d',time.localtime(time.time())), user_id)
		try:
		   self.cursor.execute(sql)
		   self.db.commit()
		except:
		   return -1

		file_obj = open('tweets_1_2/' + screen_name + '.txt','w')

		while len(tweets) > 0:
			for tt in tweets:
				try:
					file_obj.write(str(tt.id) + "\t" + str(tt.retweet_count) + "\t" + str(tt.favorite_count) + "\t" + tt.created_at.encode('utf-8') + "\n")
					file_obj.write(tt.text.replace(u'\xa0', u' ').replace('\n','  ').encode("utf-8") + "\n")
				except Exception as e1:
					print e1
					continue
			try:
				# RT @taylorswift13: So much love...(retweet)
				# tag #word  @user
				api = self.api[self.apiIndex]
				tweets = api.GetUserTimeline(user_id = user_id, count = 200, max_id = tweets[-1].id - 1)

			except Exception as e:
				print screen_name + ": get timeline failed"
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
								try:
									tweets = api.GetUserTimeline(user_id = user_id, count = 200, max_id = tweets[-1].id - 1)
									print 'hhd.....'
								except Exception as e3:
									print e3
									return
							continue
					except Exception as e2:
						print e2
						continue
				continue
				return

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