from google.cloud import language_v1
import sys
import tweepy
import string
import re
import time

def sample_analyze_sentiment(text_content):

    client = language_v1.LanguageServiceClient()

    type_ = language_v1.Document.Type.PLAIN_TEXT

    document = {"content": text_content, "type_": type_}

    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})

    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(u"Document sentiment magnitude: {}".format(response.document_sentiment.magnitude))
    for sentence in response.sentences:
        print(u"Sentence text: {}".format(sentence.text.content))
        print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))
    print(u"Language of the text: {}".format(response.language))

def get_tweets(text,api):

    # filter tweets without retweets, media and native_video
    keywords=''
    search_keywords=keywords+text+'-filter:retweets -filter:media -filter:native_video'

    # search for the full_text tweet by param tweet_mode='extended'
    tweets_find = api.search(search_keywords,lang='en',count='5',tweet_mode='extended')

    tweets_list=[]
    for search_tweet in tweets_find:
        tweets_list.append(search_tweet.full_text)

    i = 0
    for tweet in tweets_list:
        # remove hashtags, mentions, urls, emojis, etc.
        tweet = re.sub(r'#\w+ ?', '', tweet)
        tweet = re.sub(r'@\w+ ?','',tweet)
        tweet = re.sub(r'(?:\@|http?\://|https?\://|www)\S+', '', tweet)
        #tweet = re.sub(r'<3', ' ', tweet)
        tweet = re.sub(u'[\U00010000-\U0010ffff\\uD800-\\uDBFF\\uDC00-\\uDFFF]','',tweet)
        tweet = re.sub(r'\n', ' ', tweet)
        i = i+1
        print('\nNumber: {}   Keyword: {} '.format(i, text))
        sample_analyze_sentiment(tweet)

def get_keywords_from_input(keywords):
    keywords_list=keywords.split(',')
    for index in range(len(keywords_list)):
        keywords_list[index] = keywords_list[index].strip()
    return keywords_list

def get_keywords_from_param():
    args = sys.argv
    return args[1:]

def main():
    start = time.time()

    consumer_key = "ZVKdMXRwNzz5FLR2VoXltA6G3"
    consumer_secret = "DxfJ5oupjvOewjLoMwlRxhafGTHLPyQ9lhhWGCdgVfyGYAupXd"
    access_key = "1441095844367720452-04LIPcoXYHhc7iiYVsR9oeDZAos2hQ"
    access_secret = "I17DHdaUVUgWfY8ebW1Hq9wytftxKyQbFP8XWcRfzR6fR"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    keywords = get_keywords_from_param()
    if keywords != []:
        flag = input('You want to search {}. y/n: '.format(''.join(keywords)))
        while (flag != 'y' and flag != 'n'):
             flag = input('Please choose exactly y/n: ')
        while (flag == 'n'):
            keywords = input('You need to provide at least one keyword.\nYou can use comma to split.\nEmpty input will be seen as stop program.\nNow please give me keywords:\n')
            if keywords == '':
                print('Program stop')
                return 0
            else:
                keywords = get_keywords_from_input(keywords)
                flag = input('You want to search {}. y/n: '.format(' and '.join(keywords)))
                while (flag != 'y' and flag != 'n'):
                    flag = input('Please choose exactly y/n: ')
        
    else:
        flag = 'n'
        while (flag == 'n'):
            keywords=input('You need to provide at least one keyword.\nYou can use comma to split.\nEmpty input will be seen as stop program.\nNow please give me keywords:\n')
            if keywords == '':
                print('Program stop')
                return 0
            else:
                keywords = get_keywords_from_input(keywords)
                flag = input('You want to search {}. y/n: '.format(' and '.join(keywords)))
                while (flag != 'y' and flag != 'n'):
                    flag = input('Please choose exactly y/n: ')

    for keyword in keywords:
        tweets=get_tweets(keyword,api)

    end = time.time()
    return end-start

if __name__=='__main__':
    main()
