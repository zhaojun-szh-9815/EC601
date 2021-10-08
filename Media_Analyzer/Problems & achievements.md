The content of tweets is quite difficult to analyze because it always contains many items that should not be in sentences, for example, pictures, videos, emojis, etc.

Although we can remove these items by 're', the sentences are not integrated at al, especially emoji.
It is because the emojis represents emotion of the auther. For example, a sentence 'Python is good!', the sentence cannot be analyzed if the word 'good' is replaced by emoji.
Sometimes, the tweet focus on its picture or video so that the text is too less to analyze.

Because of these limitation, there are only about 20 or 30 percent of tweets can given ideal feedback after simple analysis.

<div align=center><img width="721" alt="Social_Media2" src="https://user-images.githubusercontent.com/55321300/136622315-cb0560a9-ad98-4cfc-80ff-45c09e8dd068.PNG">


<div align=left>In the test case, 'Genshin' is the keyword. The Twitter API filter the tweets without retweet, media, and native_video, and provide the full_text to the program.
The program will preprocess the tweets by removing hashtags, mentions, URLs, and emojis. Then sentiment analyze will start.

The first and the third tweet has obvious sentiments. and NLP gives the right feedback.
But the rest tweets do not have obvious sentiments, even sometimes can not understand what the tweet want to say, so the score given by NLP can only for reference.
  
In conclusion, the tweets which are searched from the whole community are hard to analyze.
A better solution will be trying to create a database to test the analyzer, but it is not match our purpose 'Media Analysis'.
So the score provided by Media Analyzer maybe can only for reference, the details still need human to explore.
