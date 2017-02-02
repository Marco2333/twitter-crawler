import twitter

# import tweepy
# auth = tweepy.OAuthHandler('bRJ4nxfQ1lQpc0b9OiGyznwTP', 'duDNQlvxtYInexf8kBiSTUwAuaskty4iGd6HnPKfoWzLoSvJgc')
# auth.set_access_token('716652054446379008-4wz9tWCPDUa61FglUqrhk58zmJmtnP2', 'hNFCesJ2rADFcmIljjEmywxGcDc6HrV6ORGZqrqNDWLXF')
# api = tweepy.API(auth)
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print tweet.text

class Crawler:
	def __init__(self):
		self.api = twitter.Api(consumer_key='bRJ4nxfQ1lQpc0b9OiGyznwTP',
	                      consumer_secret='duDNQlvxtYInexf8kBiSTUwAuaskty4iGd6HnPKfoWzLoSvJgc',
	                      access_token_key='716652054446379008-4wz9tWCPDUa61FglUqrhk58zmJmtnP2',
	                      access_token_secret='hNFCesJ2rADFcmIljjEmywxGcDc6HrV6ORGZqrqNDWLXF')

		
def getUserTweets(screen_name):
	api = twitter.Api(consumer_key='bRJ4nxfQ1lQpc0b9OiGyznwTP',
	                      consumer_secret='duDNQlvxtYInexf8kBiSTUwAuaskty4iGd6HnPKfoWzLoSvJgc',
	                      access_token_key='716652054446379008-4wz9tWCPDUa61FglUqrhk58zmJmtnP2',
	                      access_token_secret='hNFCesJ2rADFcmIljjEmywxGcDc6HrV6ORGZqrqNDWLXF')
	
	# get a specific user's timeline
	tweets = api.GetUserTimeline(screen_name = screen_name, count = 200)
	all_tweets = tweets[0].user.statuses_count
	# for s in tweets:
	# 	print s.id
	# return
	
	file_obj = open('tweets123/' + screen_name + '.txt','a')
	while all_tweets > 0:
		for tt in tweets:
			length = len(tweets)
			# if tt.id < min_id:
				# print 'hh'
				# return
			# print (type(tt.id_str), type(tt.retweeted), type(tt.favorite_count), type(tt.created_at))
			file_obj.write(str(tt.id) + "\t" + str(tt.retweeted) + "\t" + str(tt.retweet_count) + "\t" + str(tt.favorite_count) + "\t" + tt.created_at.encode('utf-8') + "\n")
			file_obj.write(tt.text.replace(u'\xa0', u' ').replace('\n','  ').encode("utf-8") + "\n")
			# print tt.id
			# print tt.retweeted
			# print tt.retweet_count
			# print tt.favorite_count
			# print tt.created_at
			# RT @taylorswift13: So much love, pride...(retweet)
			# tag #word  @user
			# print s.text
		# try:
		tweets = api.GetUserTimeline(screen_name = screen_name, count = 200, since_id = tweets[-1].id + 1)
		# except:
			# print len(tweets)
			# print length
			# return
		
		all_tweets = all_tweets - length
	file_obj.close()

# getUserTweets('realDonaldTrump')
getUserTweets('billgates')
# getUserTweets('mrmarcohan')


