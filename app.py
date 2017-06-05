#coding=utf-8
import urllib
import urllib2
import MySQLdb
import config
import time
import cookielib
import random
import re
import socket
from bs4 import BeautifulSoup
from pybloom import BloomFilter

class Crawler:
	def __init__(self):	

	
		headers = {    
			'User-Agent':config.USER_AGENT
		}   

		for i in range(10):
			request = urllib2.Request("https://api.douban.com/v2/book/6548683/tags", headers = headers)
			response = urllib2.urlopen(request)
			pageHtml = response.read()
			print i


		file_obj = open('a.html','w')
		file_obj.write(pageHtml)
		file_obj.close()

		# soup = BeautifulSoup(pageHtml, 'html.parser')
		# name = soup.select_one(".cd__headline")
		# print name

		return
		
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
		name = soup.select_one(".ProfileHeaderCard-nameLink").text

		


	def getBasicInfo(self):
		url = "https://twitter.com/" + self.currentUser

		try:
			request = urllib2.Request(url, headers = self.headers[0])
			response = urllib2.urlopen(request, timeout = 5)
			pageHtml = response.read()
			# file_obj = open('a.html','w')
			# file_obj.write(pageHtml)
			# file_obj.close()
		except:
			print "basic info 请求超时"
			return -1

		soup = BeautifulSoup(pageHtml, 'html.parser', from_encoding="unicode")

		name = soup.select_one(".ProfileHeaderCard-nameLink").text
		screenname = soup.select_one(".u-linkComplex-target").text
		bio = soup.select_one(".ProfileHeaderCard-bio").text
		jd = soup.select_one(".ProfileHeaderCard-joinDateText")['title']
		location = soup.select_one(".ProfileHeaderCard-locationText").text
		try:
			jd = jd.split(' ')[2]
			joindate = re.sub('[^\d]+',"-",jd)
			joindate = joindate[0 : -1]
		except:
			joindate = ""

		# joindate = jdlist[5] + "-" + self.months[jdlist[4]] + "-" + jdlist[3]

		try:
			tn = soup.select_one(".ProfileNav-item--tweets") \
				.select_one(".ProfileNav-stat--link")['title']
			tweetNum = tn.split(' ')[0].replace(',','')
			if int(tweetNum) < 60:
				return -1
		except:
			return -1
		
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
		   return -1

		tweets = soup.select(".js-stream-item")
		file_obj = open('tweet/' + self.currentUser + '.txt','a')
		for i in range(len(tweets)):
			try:
				tt = tweets[i].select_one(".js-tweet-text-container").text.replace(u'\xa0', u' ').replace('\n',' ')
				file_obj.write(tt.encode('utf-8'))
				file_obj.write("\n")
			except:
				continue
			try:
				timestamp = tweets[i].select_one(".stream-item-header").select_one(".js-short-timestamp")['data-time']
				user = tweets[i].select_one(".stream-item-header").select_one(".username").select_one('b').text
				itemFooter =  tweets[i].select_one(".stream-item-footer")
				reply = itemFooter.select_one(".ProfileTweet-action--reply").select_one(".ProfileTweet-actionCount")['data-tweet-stat-count']
				retweet = itemFooter.select_one(".ProfileTweet-action--retweet").select_one(".ProfileTweet-actionCount ")['data-tweet-stat-count']
				favorite = itemFooter.select_one(".ProfileTweet-action--favorite").select_one(".ProfileTweet-actionCount ")['data-tweet-stat-count']
			except:
				print "tweets bottom error"
			file_obj.write(user + " " + timestamp + " " + reply + " " + retweet + " " + favorite)
			file_obj.write('\n')
		file_obj.close()		


spider = Crawler()
