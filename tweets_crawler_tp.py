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
		self.apiIndex = 0
		self.sleep_count = 0
		# self.months = dict(Jan = '1', Feb = '2', Mar = '3', Apr = '4', \
		# 				May = '5', Jun = '6', Jul = '7', Aug = '8', \
		# 				Sep = '9', Oct = '10', Nov = '11', Dec = '12')

		# db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		# cursor = db.cursor()
		# self.cursor = cursor
		# self.db = db
		# self.sleep_count = 0
		self.getAllUsersTweets()
		# self.getUserTweets('17919972')
		# print api[0].GetUser(screen_name='mrmarcohan')


	def getAllUsersTweets(self):
		name_list = ['bbceducation', 'BBCBusiness', 'CNNPolitics', 'cnntech', 'CNNMoney', 'CNNent', 'cnnsportsnews', 'CNNbelief', 'USDA', 'MilitaryTimes', 'BBCScienceNews', 'BBCTech', 'BBCLearning', 'BBCSchoolReport']

		for ii in name_list:
			try:
				self.getUserTweets(ii)
				print ii + " finished..."
			except Exception as e:
				print ii + " failed"
				print e
				continue
	

	def getUserTweets(self, screen_name):
		api = self.api[self.apiIndex]
		self.apiIndex = (self.apiIndex + 1) % self.apiCount
		try:
			# get a specific user's timeline
			tweets = api.GetUserTimeline(screen_name = screen_name, count = 200)
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
							self.getUserTweets(screen_name)
							return
						
				except Exception as e2:
					print e2
			return

		if len(tweets) <= 0:
			return

		

		file_obj = open('tweets/' + screen_name + '.txt','w')

		while len(tweets) > 0:
			for tt in tweets:
				try:
					# file_obj.write(str(tt.id) + "\t" + str(tt.retweet_count) + "\t" + str(tt.favorite_count) + "\t" + tt.created_at.encode('utf-8') + "\n")
					file_obj.write(tt.text.replace(u'\xa0', u' ').replace('\n','  ').encode("utf-8") + "\n")
				except Exception as e1:
					print e1
					continue
			try:
				# RT @taylorswift13: So much love...(retweet)
				# tag #word  @user
				api = self.api[self.apiIndex]
				self.apiIndex = (self.apiIndex + 1) % self.apiCount
				tweets = api.GetUserTimeline(screen_name = screen_name, count = 200, max_id = tweets[-1].id - 1)

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
							continue
					except Exception as e2:
						print e2
						continue
				continue
				return

		file_obj.close()

		
spider = Crawler()