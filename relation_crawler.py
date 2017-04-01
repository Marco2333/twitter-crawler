import time
# import threading

# from config import THREAD_NUM
from twitter import error
from api import ApiList, ApiCount
# from database import Mysql

class RelationCrawler:
	def __init__(self):
		self.api_index = 0
		
	def get_friendids(self,
                      user_id = None,
                      screen_name = None,
                      cursor = None,
                      count = None,
                      total_count = None,
                      skip_status = False,
                      include_user_entities = True):

		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		friends = api.GetFriendIDs(user_id = user_id,
			                      screen_name = screen_name,
			                      cursor = cursor,
			                      count = count,
			                      total_count = total_count,
			                      skip_status = skip_status,
			                      include_user_entities = include_user_entities)

		return friends

	def get_friendids_paged(self,
	                        user_id = None,
	                        screen_name = None,
	                        cursor = -1,
	                        stringify_ids = False,
	                        count = 5000):
		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		friends = api.GetFriendIDsPaged(user_id = user_id,
					                    screen_name = screen_name,
					                    cursor = cursor,
					                    count = count,
					                    stringify_ids = stringify_ids)

		return friends

	def get_friends(self,
                    user_id = None,
                    screen_name = None,
                    cursor = None,
                    count = None,
                    total_count = None,
                    skip_status = False,
                    include_user_entities = True):

		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		friends = api.GetFriends(user_id = user_id,
			                     screen_name = screen_name,
			                     cursor = cursor,
			                     count = count,
			                     total_count = total_count,
			                     skip_status = skip_status,
			                     include_user_entities = include_user_entities)

		return friends

	def get_friends_paged(self,
                   		  user_id = None,
                          screen_name = None,
                          cursor = -1,
                          count = 200,
                          skip_status = False,
                          include_user_entities = True):

		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		friends = api.GetFriendsPaged(user_id = user_id,
				                      screen_name = screen_name,
				                      cursor = cursor,
				                      count = count,
				                      skip_status = skip_status,
				                      include_user_entities = include_user_entities)

		return friends

	def get_all_friendids(user_id = None,
	                      screen_name = None,
	                      skip_status = False,
	                      include_user_entities = True)

		cursor = -1
		api_index = 0
		sleep_count = 0

		while cursor != 0:
			api = ApiList[api_index]
			api_index = (api_index + 1) / ApiCount

			try:
				out = api.GetFriendIDsPaged(user_id = user_id, cursor = cursor, count = 5000)
				cursor = out[0]
				friend_list = out[2]
				# for fl in friend_list:
				# 	file_obj.write(str(fl) + " ")

			except error.TwitterError as te:
				if te.message[0]['code'] == 88:
					sleep_count += 1
					if sleep_count == ApiCount:
						print "sleeping..."
						sleep_count = 0
						time.sleep(700)
					continue
				else:
					continue
			except Exception as e:
			# 	file_obj.write("\n")
			# 	file_obj.close()		
				continue


	def get_followersids(self,
	                     user_id = None,
	                     screen_name = None,
	                     cursor = None,
	                     count = None,
	                     total_count = None,
	                     skip_status = False,
	                     include_user_entities = True):

		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		followerss = api.GetFollowersIDs(user_id = user_id,
					                     screen_name = screen_name,
					                     cursor = cursor,
					                     count = count,
					                     total_count = total_count,
					                     skip_status = skip_status,
					                     include_user_entities = include_user_entities)

		return followerss

	def get_followersids_paged(self,
		                       user_id = None,
		                       screen_name = None,
		                       cursor = -1,
		                       stringify_ids = False,
		                       count = 5000):

		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		followerss = api.GetFollowersIDsPaged(user_id = user_id,
						                 	  screen_name = screen_name,
						                 	  cursor = cursor,
						                 	  count = count,
						                 	  stringify_ids = stringify_ids)

		return followerss

	def get_followerss(self,
	                   user_id = None,
	                   screen_name = None,
	                   cursor = None,
	                   count = None,
	                   total_count = None,
	                   skip_status = False,
	                   include_user_entities = True):

		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		followerss = api.GetFollowerss(user_id = user_id,
				                       screen_name = screen_name,
				                       cursor = cursor,
				                       count = count,
				                       total_count = total_count,
				                       skip_status = skip_status,
				                       include_user_entities = include_user_entities)

		return followerss

	def get_followerss_paged(self,
	                   		 user_id = None,
	                         screen_name = None,
	                         cursor = -1,
	                         count = 200,
	                         skip_status = False,
	                         include_user_entities = True):

		if user_id == None and screen_name == None:
			return

		api = ApiList[self.api_index]
		self.api_index = (self.api_index + 1) / ApiCount

		followerss = api.GetFollowerssPaged(user_id = user_id,
					                        screen_name = screen_name,
					                        cursor = cursor,
					                        count = count,
					                        skip_status = skip_status,
					                        include_user_entities = include_user_entities)

		return followerss

	def get_all_followersids(user_id = None,
		                     screen_name = None,
		                     skip_status = False,
		                     include_user_entities = True)

		cursor = -1
		api_index = 0
		sleep_count = 0

		while cursor != 0:
			api = ApiList[api_index]
			api_index = (api_index + 1) / ApiCount

			try:
				out = api.GetFollowersIDsPaged(user_id = user_id, cursor = cursor, count = 5000)
				cursor = out[0]
				friend_list = out[2]
				# for fl in friend_list:
				# 	file_obj.write(str(fl) + " ")

			except error.TwitterError as te:
				if te.message[0]['code'] == 88:
					sleep_count += 1
					if sleep_count == ApiCount:
						print "sleeping..."
						sleep_count = 0
						time.sleep(700)
					continue
				else:
					continue
			except Exception as e:
			# 	file_obj.write("\n")
			# 	file_obj.close()		
				continue