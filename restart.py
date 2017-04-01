import MySQLdb
import config

db = MySQLdb.connect(config.DB_HOST, config.DB_USER, config.DB_PASSWD, config.DB_DATABASE)
db.set_character_set('utf8')
cursor = db.cursor()

for i in range(2, 3):
	print str(i) + "..."
	
	sql = "insert into user_fill select * from user_fill_%s" % i

	try:
		cursor.execute(sql)
		db.commit()
	except Exception as e:
		print e
		break

	sql = "delete from user_userid_%s where user_id in (select user_id from user_fill_%s)" % (i, i)

	try:
		cursor.execute(sql)
		db.commit()
	except Exception as e:
		print e
		break

	sql = "delete from user_fill_%s" % i

	try:
		cursor.execute(sql)
		db.commit()
	except Exception as e:
		print e
		break

db.close()
		
