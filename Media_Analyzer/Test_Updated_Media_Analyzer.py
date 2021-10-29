import Updated_Media_Analyzer as MA
import pytest
import tweepy

def test_get_keyword_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _:"Genshin,Boston University")
    keywords_input = input('give me keywords (use comma to split):')
    get_keywords = MA.get_keywords_from_input(keywords_input)
    assert get_keywords == ['Genshin','Boston University']

def test_get_keyword_param():
    get_keywords = MA.get_keywords_from_param()
    assert get_keywords == ['Media_Analyzer/Test_Updated_Media_Analyzer.py']

