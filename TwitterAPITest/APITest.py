import tweepy

consumer_key = "******"
consumer_secret = "******"
access_key = "******"
access_secret = "******"


# Create an Api instance.
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

specific_user="@GenshinImpact"

# print me
me = api.me()
print("my id: ",me.id_str, "\nmy screen name: ",me.screen_name)

# get user
user = api.get_user(specific_user)
print("\nUser id: ",user.id_str,"\nScreen Name: ",user.screen_name)

# User_timeline: Returns the 5 most recent statuses posted from the authenticating user or the user specified.
recent_tweet = api.user_timeline(user.id_str,count=5)
for tweet in recent_tweet:
    print('tweet id: ',tweet.id,'\ntweet text: ',tweet.text)

# get a single status specified by the tweet ID parameter
Astatus = api.get_status(recent_tweet[0].id)
print('\nthe lastest status: ',Astatus.text)

# get friends, api.friends_ids(id/screen_name/user_id, [cursor]) can also return the IDs of users being followed by the specified user.
user_friends = api.friends(user.id_str)
for friend in user_friends:
    print('\nfriend id: ',friend.id_str,'\nfriend screen name: ',friend.screen_name)

# a user's followers ordered in which they were added, api.followers_ids(id/screen_name/user_id) can also return the IDs of users following the specified user.
user_followers = api.followers(user.id_str, count=10)
for follower in user_followers:
    print('\nfollower id: ',follower.id_str,'\nfollower screen name: ',follower.screen_name)

# a search for 10 users related to 'Boston'
users_find = api.search_users('Boston',count=10)
for search_user in users_find:
    print('\nuser id: ',search_user.id_str,'\nuser screen name: ',search_user.screen_name)

# show friendships
friendship_result = api.show_friendship(source_id=me.id_str,target_id=user.id_str)
print('\n')
print(friendship_result[0].screen_name,"following",friendship_result[1].screen_name,"?:", friendship_result[0].following)
print(friendship_result[0].screen_name,"followed by ",friendship_result[1].screen_name,"?:", friendship_result[0].followed_by)

# search 20 tweets about 'Genshin' in Chinese, and print the text of the tweet and hashtags
tweets_find = api.search('Genshin',lang='zh',count='20')
for search_tweet in tweets_find:
    print('\n')
    print('tweet text:',search_tweet.text)
    hashtags=[]
    for tag_inf in search_tweet.entities['hashtags']:
        hashtags.append(tag_inf['text'])
    if len(hashtags)!=0:
        print('tweet hashtag:',hashtags)
print('\n')

# the top 50 trending topics for a specific WOEID
# Global information is available by using 1 as the WOEID.
trends_worldwide = api.trends_place(1)
data = trends_worldwide[0]
trends = data['trends']
trend_list=[]
for trend in trends:
    trend_list.append(trend['name'])
print('Trends:',trend_list)

# Given id of a place, provide more details about that place. The place id should be requested on https://api.twitter.com/1.1/geo/id/:place_id.json
# Thanks to https://iq.opengenus.org/geo-api-twitter/
details = api.geo_id('df51dec6f4ee2b2c')
print('\nthe full name of the place:',details.full_name)
