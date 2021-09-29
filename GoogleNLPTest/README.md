It is a simple test to Google Natrual Language API, and mainly focus on the sentiment analyzing. The program is tested on Google Cloud SDK Shell.

Installing and meeting all the requirements takes a long time, but the following document can be a great help for beginners.
https://cloud.google.com/natural-language/docs/setup

The content of the program is mainly refers to the sample document provided by Google.
https://cloud.google.com/natural-language/docs/analyzing-sentiment.
You can also find the comments Google provided for the function code.
By removing specified language in Google's sample, the test can detect the language automatically.
It also provided other examples, such as entities analyzing, syntax analyzing, etc.

Here is the output of my test:
<div align=center><img width="665" alt="GoogleNLP1" src="https://user-images.githubusercontent.com/55321300/135214942-5677ed8b-69e5-42f2-92d4-2a1c6e63ec48.PNG">
In this case, the API did very well, except the third test. The first sentence should be a middle or even positive sentiment, but the API gives -0.4.

<div align=center><img width="510" alt="GoogleNLP2" src="https://user-images.githubusercontent.com/55321300/135215833-4cbf86e1-b31d-415f-8602-c5113c9ef042.PNG">
In this case, the test got a Chinese input. The content of two input are all "I'm tired today. But we really had a good time.".
The first test produced a strange output. In Chinese, the character '痛' means 'painful', but the word '痛快' means 'joyful'.
So it seems that the API look for words or characters which contains important emotion.
