import twitter

# import tweepy

# auth = tweepy.OAuthHandler('bRJ4nxfQ1lQpc0b9OiGyznwTP', 'duDNQlvxtYInexf8kBiSTUwAuaskty4iGd6HnPKfoWzLoSvJgc')
# auth.set_access_token('716652054446379008-4wz9tWCPDUa61FglUqrhk58zmJmtnP2', 'hNFCesJ2rADFcmIljjEmywxGcDc6HrV6ORGZqrqNDWLXF')
# api = tweepy.API(auth)

# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print tweet.text


api = twitter.Api(consumer_key='bRJ4nxfQ1lQpc0b9OiGyznwTP',
                      consumer_secret='duDNQlvxtYInexf8kBiSTUwAuaskty4iGd6HnPKfoWzLoSvJgc',
                      access_token_key='716652054446379008-4wz9tWCPDUa61FglUqrhk58zmJmtnP2',
                      access_token_secret='hNFCesJ2rADFcmIljjEmywxGcDc6HrV6ORGZqrqNDWLXF')
# get my timeline
# statuses = api.GetUserTimeline()
# get a specific user's timeline
statuses = api.GetUserTimeline(screen_name = "taylorswift13")
print([s.text for s in statuses])

