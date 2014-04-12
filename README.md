This is a course project of Social Networks at New York University

Configration
---
* install tweepy: `pip install tweepy`
* install [NLTK](http://www.nltk.org/index.html): `sudo pip install -U numpy` (optional), `sudo pip install -U pyyaml nltk`


Design
---
Rank twitters  April 12 2014
wenjie chen

1. collectTwit.py is a few modification based on twit.py. It collects twitter messages into a 'trainData.csv' or 'testData.csv' using '|' as delimiter. 

2. maxentropyDemo.py is a demo for using maximum entropy classifier

3. rank.py uses maximum entropy classifier to get the probability that a twitter (in test_data_csv file) talks about event 1. Event 1 is the event that we want to predict. Event 0 is the event we don't care

in 'data' folder, trainData_topic_party.csv is used to model maxentropy classifier, whose event 1 is 'party', 'testData_beer_party_fire.csv' is collection of twitters containing key word 'beer', 'party' or 'fire'. The rank result gives top 10 twitters indicating where has a party.

Run command: `python rank.py`

ATTENTION: in trainData.csv, the delimiter is ',', but in testData.csv, the delimiter is '|'
Using '|' is better, because a twitter message might have ',', which leads to uncorrectly separation. But the trainData is collected two days ago. I'll fix it when create new train data at the next time.
