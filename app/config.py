# -*- coding:utf-8 -*-

#################################### Basic Config #############################
THREAD_NUM = 3   # 线程数量
USER_AGENT = '''Mozilla/5.0 (Windows NT 6.3; WOW64) 
				AppleWebKit/537.36 (KHTML, like Gecko) 
				Chrome/55.0.2883.87 Safari/537.36'''
############################## Database Config #####################################
# MySQL配置
MYSQL = {
	'DB_USER': 'root',
	'DB_PASSWORD': 'aliyunmysql@',
	# 'DB_PASSWORD': '283319',
	'DB_HOST': '127.0.0.1',
	'DB_DATABASE': 'twitter',
	'DB_CHARSET': 'utf8mb4'
}

# MongoDB配置
MONGO_DB = {
	'DB_HOST': '127.0.0.1',
	'DB_PORT': 27017,
	'DB_DATABASE': 'twitter'
}
############################## App Config(58) #####################################
APP_INFO = [{
		#========================50=======================================
		'consumer_key':'bRJ4nxfQ1lQpc0b9OiGyznwTP',
		'consumer_secret':'duDNQlvxtYInexf8kBiSTUwAuaskty4iGd6HnPKfoWzLoSvJgc',
		'access_token_key':'716652054446379008-4wz9tWCPDUa61FglUqrhk58zmJmtnP2',
		'access_token_secret':'hNFCesJ2rADFcmIljjEmywxGcDc6HrV6ORGZqrqNDWLXF'
	}
]
####################################################################################