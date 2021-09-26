It is a train to use Twitter API. The test uses ‘tweepy’ library, and it is completed based on the reference which is ‘https://github.com/tweepy/tweepy/blob/v3.10.0/docs/api.rst’.

<div align=left>me() function returns a user object which is yourself, and print the user id and screen name in this test.
<div align=center><img width="188" alt="TwitterAPI_1" src="https://user-images.githubusercontent.com/55321300/134827950-93426135-9eb9-472f-97b4-71460384026f.PNG">

<div align=left>get_user() function returns a user object which is based on the parameter, and print the user id and screen name in this test, which is ‘GenshinImpact’.
<div align=left>user_timeline() function returns a list of status object, and print the tweet id and the text in this test.
<div align=center><img width="947" alt="TwitterAPI_2" src="https://user-images.githubusercontent.com/55321300/134827953-8ae3b748-6d32-460a-9f18-e9a1d141beb5.PNG">

<div align=left>get_status() function returns a status object which based on the parameter, and in this text, print the last status.
<div align=center><img width="548" alt="TwitterAPI_3" src="https://user-images.githubusercontent.com/55321300/134827969-ad8d0b1b-c010-47e9-b1cb-2f711160b66d.PNG">

<div align=left>friends(), followers(), search_user() return a list of user object based on the parameter, and print the user id and screen name in this test.
<img width="290" alt="TwitterAPI_4" src="https://user-images.githubusercontent.com/55321300/134827976-8627a82d-b34d-4e8d-98bf-1658f5ba18da.PNG">
<img width="258" alt="TwitterAPI_5" src="https://user-images.githubusercontent.com/55321300/134827978-1d2e3002-8222-419d-98de-b91a45222b24.PNG">
<img width="301" alt="TwitterAPI_6" src="https://user-images.githubusercontent.com/55321300/134827981-28547b9c-4684-40ff-98bd-db5d6c1cee4e.PNG">

<div align=left>show_friendship() return the relationship between the two parameters, which is my screen name and ‘GenshinImpact’.
<div align=center><img width="333" alt="TwitterAPI_7" src="https://user-images.githubusercontent.com/55321300/134827983-e58eb298-e973-44bc-9a98-bf32dc0bc3ad.PNG">

<div align=left>search() function return a list of status object, and print text and hashtags in this test.
<div align=center><img width="654" alt="TwitterAPI_8" src="https://user-images.githubusercontent.com/55321300/134827989-2b75c10b-e083-47e3-a027-ac96e86afc33.PNG">

<div align=left>trend_place() and geo_id() can return trends and details based on location ID parameter. Getting the location ID needs to make request to Twitter API.
<div align=left>It is a special case in this test, which is trends in worldwide and Presidio, San Francisco in details.
<div align=center><img width="1269" alt="TwitterAPI_9" src="https://user-images.githubusercontent.com/55321300/134827990-dbff6658-d6cc-47b4-9c06-70792c66876d.PNG">
