#coding=utf-8
import urllib
import urllib2
import MySQLdb
import config
import time
# import chardet
import cookielib
from bs4 import BeautifulSoup

# #登录教务系统的URL
# 
# 
# #利用cookie请求访问另一个网址，此网址是成绩查询网址
# 
class Crawler:
	def __init__(self):

		#初始化headers
		# filename = 'cookie.txt'

		#声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
		# cookie = cookielib.MozillaCookieJar(filename)
		# opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		# postdata = urllib.urlencode({
		# 			'session[username_or_email]':'mrmarcohan',
		# 			'session[password]':'han123456',
		# 			'authenticity_token':'f6d4aaabed56cf50ac43106ff4a561fcd21abd33'
		# 		})
		# loginUrl = 'http://https://twitter.com/login'
		# # #模拟登录，并把cookie保存到变量
		# result = opener.open(loginUrl, postdata)
		# cookie.save(ignore_discard=True, ignore_expires=True)

		# return
		# gradeUrl = 'http://jwxt.sdu.edu.cn:7890/pls/wwwbks/bkscjcx.curscopre'
		# #请求访问成绩查询网址
		# result = opener.open(gradeUrl)
		# print result.read()
		# #保存cookie到cookie.txt中
		self.headers = { 'User-Agent' : config.USER_AGENT}

		request = urllib2.Request("https://twitter.com/login", headers = self.headers)
		response = urllib2.urlopen(request)
		pageHtml = response.read()
		soup = BeautifulSoup(pageHtml, 'html.parser')
		csrf = soup.find_all("input", attrs={"name": "authenticity_token"})[0]['value']

		print csrf

		headers = {    
			'User-Agent':config.USER_AGENT,
			'referer':'https://twitter.com/login'
		}    
  		
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
		print page

		file_obj = open('a.html','w')
		file_obj.write(page)
		file_obj.close()

		return 


		self.urlList = []
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
		self.getPageHtml(config.INITIAL_URL)

	def getPageHtml(self, url):
		try:
			request = urllib2.Request(url, headers = self.headers)
			response = urllib2.urlopen(request)
			pageHtml = response.read()
			# char_type = chardet.detect(pageHtml)
			# print char_type
			# return
			# response=requests.get(url)
			# response.encoding = 'utf-8' #将requests强制编码为utf_8
			self.currentUser = 'taylorswift13'
			self.getBasicInfo(pageHtml)

		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print e.reason

	def getBasicInfo(self, pageHtml):
		soup = BeautifulSoup(pageHtml, 'html.parser', from_encoding="unicode")
		# print soup.originalEncoding
		file_obj = open('a.html','w')
		file_obj.write(pageHtml)
		file_obj.close()
		return
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
			if int(tweetNum) < 10:
				print "tweetNum < 10"
				return
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
		# try:
		#    # 执行sql语句
		#    # self.cursor.execute(sql)
		#    # 提交到数据库执行
		#    # self.db.commit()
		# except:
		# 	print 1
		#    # return

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
			
			# print reply
			# print retweet
			# print favorite
			file_obj.write(user + " " + timestamp + " " + reply + " " + retweet + " " + favorite)
			file_obj.write('\n')
		file_obj.close()		

	# def getTweet(): 


	def crawlerFinish(self):
		self.db.close()

spider = Crawler()

# def get_info():
#     xuhao=[]
#     project_name=[]
#     project_strict=[]
#     project_sale_num=[]
#     project_order_num=[]
#     project_sale_area=[]
#     project_ave_price=[]

#     baseurl='http://hz.house.ifeng.com/detail/2014_10_28/50087618_'

#     page_num=1
#     url=baseurl+str(page_num)+'.shtml'
#     response=requests.get(url)
#     response.encoding = 'utf-8' #将requests强制编码为utf_8
#     # print response.encoding   查看requests的编码方式

#     soup=BeautifulSoup(response.text,'lxml')
#     arcicle=soup.find('div',{'class':'article'})
#     tr=arcicle.find_all('tr')
#     for i in range(2,len(tr)-1):
#         td=tr[i].find_all('td')

#         xuhao.append(td[0].string.strip())
#         project_name.append(td[1].string.strip())
#         project_strict.append(td[2].string.strip())
#         project_sale_num.append(td[3].string.strip())
#         project_order_num.append(td[4].string.strip())
#         project_sale_area.append(td[5].string.replace('㎡','').strip())
#         project_ave_price.append(td[6].string.strip())

#     df=DataFrame(xuhao,columns=['xuhao'])
#     df['name']=DataFrame(project_name)
#     df['strict']=DataFrame(project_strict)
#     df['sale_num']=DataFrame(project_sale_num)
#     df['order_num']=DataFrame(project_order_num)
#     df['area']=DataFrame(project_sale_area)
#     df['ave_price']=DataFrame(project_ave_price)
#     return df


# if __name__=='__main__':

#     page=get_info()
#     print page