import tweepy

# 填入你的认证信息
#consumer_key = "API / Consumer Key here",
#    consumer_secret="API / Consumer Secret here",

consumer_key = '9lsn2k1yP3svtFkn0OKo3iYVA'
consumer_secret = 'PeJUjYpotXDKsXWlLr9MdCK471H3BrDwvWZhW0lzs8IurjkvmC'
access_token = "2782127138-jIOefOy8aJjsUTGWJsUARKrUS8Q1Yubb4ZNSm1v"
access_token_secret = "nt9PmpH5WpCLXKgK1I7n39Q4hWXswXXRqDVeVmwa38AwU"

bearToken = "bear token AAAAAAAAAAAAAAAAAAAAAMy5qwEAAAAA5i4KENoNebi%2F%2FTuK5pDHwPO5EvY%3D9C7S2bs94xb0LBKcms62mwySR6mhLwbmQqQ2uu8NwjM4C6q5ML"
# 进行认证并创建API连接
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# 进行搜索
for tweet in api.search_tweets(q="chat.openai.com/g/", lang="en", count =100):
    print(f"{tweet.user.name}:{tweet.text}\n")
