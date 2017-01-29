#coding=utf-8
import urllib
import urllib2
import MySQLdb
import config
import time
import Queue
import cookielib
from bs4 import BeautifulSoup


class Crawler:
	def __init__(self):

		#获取一个保存cookie的对象
		cj = cookielib.LWPCookieJar()
		#将一个保存cookie对象，和一个HTTP的cookie的处理器绑定
		cookie_support = urllib2.HTTPCookieProcessor(cj)
		#创建一个opener，将保存了cookie的http处理器，还有设置一个handler用于处理http的URL的打开
		opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
		#将包含了cookie、http处理器、http的handler的资源和urllib2对象板顶在一起
		urllib2.install_opener(opener)

		headers = {    
			'User-Agent':config.USER_AGENT,
			'referer':'https://twitter.com/login'
		}   

		request = urllib2.Request("https://twitter.com/login", headers = headers)
		response = urllib2.urlopen(request)
		pageHtml = response.read()
		soup = BeautifulSoup(pageHtml, 'html.parser')
		csrf = soup.find_all("input", attrs={"name": "authenticity_token"})[0]['value']

		postdata = {
			'session[username_or_email]':'mrmarcohan',
			'session[password]':'han123456',
			'authenticity_token':csrf,
			'scribe_log':'',
			'redirect_after_login':''
		}

		req = urllib2.Request(    
			url = 'https://twitter.com/sessions',	
			data = urllib.urlencode(postdata),
			headers = headers	
		)

		res = urllib2.urlopen(req)
		page = res.read()

		request = urllib2.Request("https://twitter.com/taylorswift13/following", headers = headers)
		response = urllib2.urlopen(request)
		pageHtml = response.read()
		
		# file_obj = open('a.html','w')
		# file_obj.write(pageHtml)
		# file_obj.close()

		# cookie = cookielib.CookieJar()
		# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		# response = opener.open('https://twitter.com')
		# for item in cookie:
		# 	print item
		# 	# if item.name == 'some_cookie_item_name':
		# 		# print item.value
		# return

		self.urlList = Queue.Queue()
		self.urlList.put(config.INITIAL_USER)
		# self.months = dict(January = 1, February = 2, March = 3, \
		# 		April = 4, May = 5, June = 6, July = 7, August = 8, \
		# 		September = 9, October = 10, November = 11, December = 12)
		self.months = dict(Jan = '1', Feb = '2', Mar = '3', Apr = '4', \
						May = '5', Jun = '6', Jul = '7', Aug = '8', \
						Sep = '9', Oct = '10', Nov = '11', Dec = '12')

		db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
		# 使用cursor()方法获取操作游标 
		cursor = db.cursor()
		self.cursor = cursor
		self.db = db
		self.getUsersInfo()

	def getUsersInfo(self):
		user = self.urlList.get()
		url = "https://twitter.com/" + user
		print url

		self.currentUser = user
		if self.getBasicInfo() != -1:
			self.getFollowing()
			self.getFollowers()

	def getBasicInfo(self):
		url = "https://twitter.com/" + self.currentUser

		try:
			request = urllib2.Request(url, headers = self.headers)
			response = urllib2.urlopen(request)
			pageHtml = response.read()

		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print e.reason
			return

		soup = BeautifulSoup(pageHtml, 'html.parser', from_encoding="unicode")

		name = soup.select_one(".ProfileHeaderCard-nameLink").text
		screenname = soup.select_one(".u-linkComplex-target").text
		bio = soup.select_one(".ProfileHeaderCard-bio").text
		jd = soup.select_one(".ProfileHeaderCard-joinDateText")['title']
		location = soup.select_one(".ProfileHeaderCard-locationText").text
		jd = jd.encode("utf-8")
		jdlist = jd.split(' ')
		joindate = jdlist[5] + "-" + self.months[jdlist[4]] + "-" + jdlist[3]

		try:
			tn = soup.select_one(".ProfileNav-item--tweets") \
				.select_one(".ProfileNav-stat--link")['title']
			tweetNum = tn.split(' ')[0].replace(',','')
			if int(tweetNum) < 50:
				return -1
		except:
			return
		
		try:
			fing = soup.select_one(".ProfileNav-item--following") \
						.select_one(".ProfileNav-stat--link")['title']
			following = fing.split(' ')[0].replace(',','')
		except:
			following = 0
		try:
			fers = soup.select_one(".ProfileNav-item--followers") \
					.select_one(".ProfileNav-stat--link")['title']
			followers = fers.split(' ')[0].replace(',','')
		except:
			followers = 0

		try:
			fates = soup.select_one(".ProfileNav-item--favorites") \
					.select_one(".ProfileNav-stat--link")['title']
			favorites = fates.split(' ')[0].replace(',','')
		except:
			favorites = 0

		# SQL 插入语句
		sql = """INSERT INTO user(screenname, name, location, joinDate, bio, tweetNum, watchNum, 
				fansNum, likeNum, created_at) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', 
				'%s', '%s', '%s')""" % (screenname, name, location, joindate, bio, tweetNum, \
				following, followers, favorites, time.strftime('%Y-%m-%d',time.localtime(time.time()))) 
		try:
		   # 执行sql语句
		   self.cursor.execute(sql)
		   # 提交到数据库执行
		   self.db.commit()
		except:
		   return

		tweets = soup.select(".js-stream-item")
		file_obj = open('tweet/' + self.currentUser + '.txt','a')
		for i in range(len(tweets)):
			tt = tweets[i].select_one(".js-tweet-text-container").text.replace(u'\xa0', u' ').replace('\n',' ')
			try:
				file_obj.write(tt.encode('utf-8'))
				file_obj.write("\n")
			except:
				print tt
				continue
			timestamp = tweets[i].select_one(".stream-item-header").select_one(".js-short-timestamp")['data-time']
			user = tweets[i].select_one(".stream-item-header").select_one(".username").select_one('b').text
			itemFooter =  tweets[i].select_one(".stream-item-footer")
			reply = itemFooter.select_one(".ProfileTweet-action--reply").select_one(".ProfileTweet-actionCount")['data-tweet-stat-count']
			retweet = itemFooter.select_one(".ProfileTweet-action--retweet").select_one(".ProfileTweet-actionCount ")['data-tweet-stat-count']
			favorite = itemFooter.select_one(".ProfileTweet-action--favorite").select_one(".ProfileTweet-actionCount ")['data-tweet-stat-count']
			
			file_obj.write(user + " " + timestamp + " " + reply + " " + retweet + " " + favorite)
			file_obj.write('\n')
		file_obj.close()		

	def getTweet(self): 
		return

	def getFollowing(self):
		url = "https://twitter.com/" + self.currentUser + "/following"
		
		try:
			request = urllib2.Request(url, headers = self.headers)
			response = urllib2.urlopen(request)
			pageHtml = response.read()

		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print e.reason
			return

		soup = BeautifulSoup(pageHtml, 'html.parser', from_encoding="unicode")

	def getFollowers(self):
		return

	def getFavorite(self):
		return 

	def crawlerFinish(self):
		self.db.close()

spider = Crawler()



# if __name__=='__main__':

#     page=get_info()
#     print page