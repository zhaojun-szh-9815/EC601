import Updated_Media_Analyzer as MA
import pytest
import tweepy

consumer_key = "******"
consumer_secret = "******"
access_key = "******"
access_secret = "******"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def test_get_keyword_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _:"Genshin,Boston University")
    keywords_input = input('give me keywords (use comma to split):')
    get_keywords = MA.get_keywords_from_input(keywords_input)
    assert get_keywords == ['Genshin','Boston University']

def test_get_keyword_param():
    get_keywords = MA.get_keywords_from_param()
    assert get_keywords == ['Test_Media_Analyse.py']

def test_get_tweets():
    keywords = 'Genshin'
    get_tweets = MA.get_tweets(keywords,api)
    assert get_tweets == None

def test_process_time():
    time_process = MA.main()
    assert time_process <= 0.5
