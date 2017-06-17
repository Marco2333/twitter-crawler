import threading

from app.database import Mysql
from app.basicinfo_crawler import BasicinfoCrawler
from app.tweets_crawler import TweetsCrawler
from app.relation_crawler import RelationCrawler

basicinfo_crawler = BasicinfoCrawler()
tweets_crawler = TweetsCrawler()
relation_crawler = RelationCrawler()

def get_users_basicinfo(user_list, table_name = "user", search_type = "user_id"):
	basicinfo_crawler.get_all_users(user_list, table_name = table_name, search_type = search_type)


def get_users_basicinfo_from_file(file_name, table_name = "user", search_type = "screen_name"):
	file = open(file_name)
	user_list = []

	while 1:
	    lines = file.readlines(100000)
	    if not lines:
	        break
	    for line in lines:
	        user_list.append(line.strip())

	basicinfo_crawler.get_all_users(user_list, table_name = table_name, search_type = search_type)


def get_users_basicinfo_from_db(sql, table_name = "user", search_type = "user_id"):
	mysql = Mysql()
	mysql.connect()

	try:
		user_list = mysql.fetchall(sql)
	except Exception as e:
		print e

	user_list = map(lambda x: x[0], user_list)

	basicinfo_crawler.get_all_users(user_list, table_name = table_name, search_type = search_type)


def get_users_tweets(user_list, collect_name = "tweets", search_type = "user_id"):
	tweets_crawler.get_all_users_timeline(user_list, collect_name = collect_name, search_type = search_type)


def get_users_tweets_from_file(file_name, collect_name = "tweets", search_type = "screen_name"):
	file = open(file_name)
	user_list = []

	while 1:
	    lines = file.readlines(100000)
	    if not lines:
	        break
	    for line in lines:
	        user_list.append(line.strip())

	tweets_crawler.get_all_users_timeline(user_list, collect_name = collect_name, search_type = search_type)


def get_users_tweets_from_db(sql, collect_name = "tweets", search_type = "screen_name"):
	mysql = Mysql()
	mysql.connect()

	try:
		user_list = mysql.fetchall(sql)
	except Exception as e:
		print e

	user_list = map(lambda x: x[0], user_list)

	tweets_crawler.get_all_users_timeline(user_list, collect_name = collect_name, search_type = search_type)


def get_users_relationship(user_list):
	user_list = list(set(user_list))
	length = len(user_list)
	if length == 0:
		return None

	thread_num = 2
	per_thread = length / thread_num

	i = 0
	thread_pool = []
	
	while i < thread_num:
		if i + 1 == thread_num:
			craw_thread = threading.Thread(target = get_users_relation_thread, 
							args = (user_list[i * per_thread : ], user_list, i * per_thread,))
		else:
			craw_thread = threading.Thread(target = get_users_relation_thread, 
							args = (user_list[i * per_thread : (i + 1) * per_thread], user_list, i * per_thread,))
		
		craw_thread.start()
		thread_pool.append(craw_thread)

		i += 1

	for thread in thread_pool:
		thread.join()


def get_users_relation_thread(user_list, all_users, start_index):
	length = len(user_list)
	all_length = len(all_users)
	table_name = 'relation'

	mysql = Mysql()
	mysql.connect()

	i = 0
	for i in range(length):
		for j in range(start_index + i + 1, all_length):

			relation = relation_crawler.save_friendship(source_user_id = user_list[i], target_user_id = all_users[j])
			fb = relation['relationship']['source']['followed_by']
			fl = relation['relationship']['source']['following']
			sql =  """INSERT INTO %s (source_user_id, target_user_id, followed_by, following) VALUES ('%s', '%s', \
			'%s', '%s')""" % (table_name, user_list[i], all_users[j], str(fb), str(fl)) 

			try:
				mysql.execute(sql)
			except Exception as e:
				print e
				continue

		
if __name__ == "__main__":
	mysql = Mysql()
	mysql.connect()

	sql = "select userid from standardusers"

	try:
		user_list = mysql.fetchall(sql)
	except Exception as e:
		print e

	user_list = map(lambda x: x[0], user_list)
	get_users_relationship(user_list)
