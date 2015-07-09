from twython import Twython
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
