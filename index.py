#coding=utf-8

import urllib2
from bs4 import BeautifulSoup

class Twitter:
	def __init__(self):
		self.initUrl = "https://twitter.com/taylorswift13"
		self.user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
		#初始化headers
		self.headers = { 'User-Agent' : self.user_agent }
		self.urlList = []
		self.getPageHtml(self.initUrl)

	def getPageHtml(self, url):
		try:
			request = urllib2.Request(url, headers = self.headers)
			response = urllib2.urlopen(request)
		    #将页面转化为UTF-8编码
			pageHtml = response.read()
			self.getPageInfo(pageHtml)

		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print e.reason

	def getPageInfo(self, pageHtml):
		soup = BeautifulSoup(pageHtml, 'html.parser')
		file_obj = open('a.html','w')
		file_obj.write(pageHtml)
		bio = soup.select_one(".ProfileHeaderCard-nameLink")
		print dir(soup)
		# print pageHtml
		print bio
		# print 123
		# print pageHtml         

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