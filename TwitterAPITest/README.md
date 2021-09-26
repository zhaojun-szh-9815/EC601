It is a train to use Twitter API. The test uses ‘tweepy’ library, and it is completed based on the reference which is ‘https://github.com/tweepy/tweepy/blob/v3.10.0/docs/api.rst’.

me() function returns a user object which is yourself, and print the user id and screen name in this test.

get_user() function returns a user object which is based on the parameter, and print the user id and screen name in this test, which is ‘GenshinImpact’.

user_timeline() function returns a list of status object, and print the tweet id and the text in this test.

get_status() function returns a status object which based on the parameter, and in this text, print the last status.

friends(), followers(), search_user() return a list of user object based on the parameter, and print the user id and screen name in this test.

show_friendship() return the relationship between the two parameters, which is my screen name and ‘GenshinImpact’.

search() function return a list of status object, and print text and hashtags in this test.

trend_place() and geo_id() can return trends and details based on location ID parameter. Getting the location ID needs to make request to Twitter API. So I use the special case in this test, which is trends in worldwide and Presidio, San Francisco in details.
