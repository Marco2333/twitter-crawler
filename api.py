import twitter
import config

class Api:
	def __init__(self):
		api_list = []
		self.api_count = 58
		for i in range(api_count):
			api_list.append(twitter.Api(consumer_key=config.APP_INFO[i]['consumer_key'],
		                      consumer_secret=config.APP_INFO[i]['consumer_secret'],
		                      access_token_key=config.APP_INFO[i]['access_token_key'],
		                      access_token_secret=config.APP_INFO[i]['access_token_secret']))
		self.api_list = api_list