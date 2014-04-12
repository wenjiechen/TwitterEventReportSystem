This is a course project of Social Networks at New York University

Configration
---
* install tweepy: `pip install tweepy`
* install [NLTK](http://www.nltk.org/index.html): `sudo pip install -U numpy` (optional), `sudo pip install -U pyyaml nltk`


Design
---
1. Each e-mail in our classifier's training data will have a label ("spam" or "ham") and a feature set. For this application, we're just going to use a feature set that is just a set of the unique words in the e-mail. Below, we'll turn this into a dictionary to feed into the NaiveBayesClassifier, but first, let's get the set.
