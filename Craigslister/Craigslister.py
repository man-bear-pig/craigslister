from twython import Twython
import MySQLdb
import sqlalchemy
import requests
from bs4 import BeautifulSoup
import datetime
from time import strptime
import pandas as pd

def parseResp(conn, crawl_id, load_new='N'):
	resp, city, active, user = genResp(conn, crawl_id)
	crawl_event_id = genCrawlEventId(conn, crawl_id)
	crawl_date = datetime.datetime.now()
	c_ = BeautifulSoup(resp.content).find_all("div", attrs={"class": "content"})
	t_ = c_[0].find_all("p", attrs={"class": "row"})
	r_ = []
	for i in t_:
		rn_ 		= [crawl_date]
		pid 		= dict(i.attrs)["data-pid"]
		try:
			pid_parent 	= dict(i.attrs)["data-repost-of"]
		except Exception:
			pid_parent = 0
			pass
		post_date	= datetime.datetime(*strptime(dict(i.find_all("time")[0].attrs)["datetime"], "%Y-%m-%d %H:%M")[:5])
		price 		= i.find_all("span", attrs={"class": "price"})[0].string.replace('$','')
		title		= i.find_all("a", attrs={"class": "hdrlnk"})[0].string
		if dict(i.find_all("a")[0].attrs)["href"][:4] == 'http':
			link 	= dict(i.find_all("a")[0].attrs)["href"]
		else:
			link 	= 'http://' + city + '.craigslist.org' + dict(i.find_all("a")[0].attrs)["href"]
		try:
			location 	= i.find_all("small")[0].string.replace('(','').replace(')','').strip().title()
		except Exception:
			location = '' 
			pass
		rn_.extend([pid, pid_parent, post_date , price, title, link, location, crawl_id, crawl_event_id])
		r_.append(rn_)
	if len(r_) == 0:
		print 'log:No records - crawl_event_id: ', str(crawl_event_id)
		return
	ids = fetchAdIds(conn, crawl_id)
	rt_ = []
	for i in r_:
		if int(i[1]) not in ids: 
			rt_.append(dict(crawl_date=i[0], 
				pid=i[1], 
				pid_parent=i[2], 
				post_date=i[3], 
				price=i[4], 
				title=i[5], 
				link=i[6], 
				location=i[7], 
				crawl_id=i[8], 
				crawl_event_id=i[9])
			)
	print len(rt_)
	if len(rt_) == 0:
		print 'log:No data returned'
		return
	if load_new == 'Y':
		conn_str ='mysql://crawler@localhost:3306/craigslister'
		conn, ad = db_ad.db_ad(conn_str)
		result = conn.execute(ad.insert(), rt_)
		load_count = result.rowcount
		print 'log:Load count - ', load_count
		reject_count = len(rt_) - load_count
 	return dict(data_raw=rt_, user=user, load_count=load_count, reject_count=reject_count)


#
#	Begin database-specific functions
#

def db(user, password, database, schema):
	conn = MySQLdb.connect(database, user, password, schema)
	return conn


def db_ad(conn_str):
	engine = sqlalchemy.create_engine(conn_str)
	metadata = sqlalchemy.MetaData()
	ad = sqlalchemy.Table('ad', metadata,
		sqlalchemy.Column('crawl_date', sqlalchemy.DateTime),
		sqlalchemy.Column('crawl_id', sqlalchemy.Integer, primary_key=True),
		sqlalchemy.Column('crawl_event_id', sqlalchemy.Integer),
		sqlalchemy.Column('post_date', DateTime),
		sqlalchemy.Column('pid', sqlalchemy.Integer, primary_key=True),
		sqlalchemy.Column('pid_parent', sqlalchemy.Integer),
		sqlalchemy.Column('title', sqlalchemy.String),
		sqlalchemy.Column('link', sqlalchemy.String),
		sqlalchemy.Column('price', sqlalchemy.Float),
		sqlalchemy.Column('location', sqlalchemy.String),
		sqlalchemy.Column('pic', sqlalchemy.String)
	)
	return engine.connect(), ad


def tweet(parse_resp):
	APP_KEY = 'ujoEmvuFwhRB4akl4W732ol5l'  # Customer Key here
	APP_SECRET = '3gZZVjWI8XpVwxe8Ih69zRZYSfAuVWYsZUO9bsDYxd0dUkkFQC'  # Customer secret here
	OAUTH_TOKEN = '3152163098-riRIzLkdwG4nlxYGY1BNVz7aMIGQtWASva6j6lZ'  # Access Token here
	OAUTH_TOKEN_SECRET = 'wxvwHUvETo8uwhzgXi00D1uNAOEKqawpqR1qHolcJlutN'  # Access Token Secret here
	twitter = Twython(APP_KEY
						,APP_SECRET
						,OAUTH_TOKEN
						,OAUTH_TOKEN_SECRET)
	new_tweet = ''
	for pr in parse_resp['data_raw']:
		new_tweet = (parse_resp['user'] 
						+ ' - ' 
						+ pr['title'][:40] 
						+ '... $' 
						+ pr['price'] 
						+ ' ' 
						+ pr['link'])
		print 'Tweet: ', new_tweet
		twitter.update_status(status=new_tweet)
