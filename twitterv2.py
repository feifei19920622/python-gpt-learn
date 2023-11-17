import tweepy

consumer_key = '9lsn2k1yP3svtFkn0OKo3iYVA'
consumer_secret = 'PeJUjYpotXDKsXWlLr9MdCK471H3BrDwvWZhW0lzs8IurjkvmC'
access_token = "2782127138-jIOefOy8aJjsUTGWJsUARKrUS8Q1Yubb4ZNSm1v"
access_token_secret = "nt9PmpH5WpCLXKgK1I7n39Q4hWXswXXRqDVeVmwa38AwU"
# 创建Tweepy认证对象
client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token,
                       access_token_secret=access_token_secret, )
# auth.set_access_token(access_token, access_token_secret)

# 创建API对象
# api = tweepy.API(auth, version="2")  # 使用Twitter API v2

# 设置搜索关键字
search_query = "Python programming"  # 你想搜索的关键字

# 执行搜索
tweets = client.search_all_tweets(query=search_query, max_results=10)  # 搜索最新的10条相关推文

# 打印搜索结果
for tweet in tweets:
    print(f"{tweet.author.username}: {tweet.text}\n")
