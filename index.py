#coding=utf-8

import urllib2
import MySQLdb
from bs4 import BeautifulSoup

class Twitter:
	def __init__(self):
		self.initUrl = "https://twitter.com/taylorswift13"
		self.user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
		#初始化headers
		self.headers = { 'User-Agent' : self.user_agent }
		self.urlList = []
		# self.months = dict(January = 1, February = 2, March = 3, April = 4, May = 5, June = 6, July = 7, August = 8, September = 9, October = 10, November = 11, December = 12)
		self.months = dict(Jan = '1', Feb = '2', Mar = '3', Apr = '4', May = '5', Jun = '6', Jul = '7', Aug = '8', Sep = '9', Oct = '10', Nov = '11', Dec = '12')

		db = MySQLdb.connect("127.0.0.1","root","root","twitter" )
		# 使用cursor()方法获取操作游标 
		cursor = db.cursor()
		self.cursor = cur 
		self.getPageHtml(self.initUrl)

	def getPageHtml(self, url):
		try:
			request = urllib2.Request(url, headers = self.headers)
			response = urllib2.urlopen(request)
			pageHtml = response.read()
			self.getPageInfo(pageHtml)

		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print e.reason

	def getPageInfo(self, pageHtml):
		soup = BeautifulSoup(pageHtml, 'html.parser')
		# file_obj = open('a.html','w')
		# file_obj.write(pageHtml)

		name = soup.select_one(".ProfileHeaderCard-nameLink").text
		screenname = soup.select_one(".u-linkComplex-target").text
		bio = soup.select_one(".ProfileHeaderCard-bio").text
		jd = soup.select_one(".ProfileHeaderCard-joinDateText")['title']
		location = soup.select_one(".ProfileHeaderCard-locationText").text
		jd = jd.encode("utf-8")
		jdlist = jd.split(' ')
		joindate = jdlist[5] + "-" + self.months[jdlist[4]] + "-" + jdlist[3]

		tn = soup.select_one(".ProfileNav-item--tweets").select_one(".ProfileNav-stat--link")['title']
		tweetNum = tn.split(' ')[0]
		fing = soup.select_one(".ProfileNav-item--following").select_one(".ProfileNav-stat--link")['title']
		following = fing.split(' ')[0]
		fers = soup.select_one(".ProfileNav-item--followers").select_one(".ProfileNav-stat--link")['title']
		followers = fers.split(' ')[0]
		fates = soup.select_one(".ProfileNav-item--favorites").select_one(".ProfileNav-stat--link")['title']
		favorites = fates.split(' ')[0]

		print followers
		print following
		print favorites

		

spider = Twitter()
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
