from google.cloud import language_v1
import argparse
import tweepy
import string
import re

def sample_analyze_sentiment(text_content):

    client = language_v1.LanguageServiceClient()

    type_ = language_v1.Document.Type.PLAIN_TEXT

    document = {"content": text_content, "type_": type_}

    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(
        u"Document sentiment magnitude: {}".format(
            response.document_sentiment.magnitude
        )
    )
    for sentence in response.sentences:
        print(u"Sentence text: {}".format(sentence.text.content))
        print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    print(u"Language of the text: {}".format(response.language))
    print('')


consumer_key = "******"
consumer_secret = "******"
access_key = "******"
access_secret = "******"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

parser = argparse.ArgumentParser()
parser.add_argument('text', help='The keywords need to be searched.')
args = parser.parse_args()

# filter tweets without retweets, media and native_video
keywords=''
search_keywords=keywords+args.text+'-filter:retweets -filter:media -filter:native_video'

# search for the full_text tweet by param tweet_mode='extended'
tweets_find = api.search(search_keywords,lang='en',count='5',tweet_mode='extended')
tweets_list=[]

for search_tweet in tweets_find:
    tweets_list.append(search_tweet.full_text)

for tweet in tweets_list:
    # remove hashtags, mentions, urls, emojis, etc.
    tweet = re.sub(r'#\w+ ?', '', tweet)
    tweet = re.sub(r'@\w+ ?','',tweet)
    tweet = re.sub(r'(?:\@|http?\://|https?\://|www)\S+', '', tweet)
    #tweet = re.sub(r'<3', ' ', tweet)
    tweet = re.sub(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]','',tweet)
    tweet = re.sub(r'\n', ' ', tweet)
    sample_analyze_sentiment(tweet)
