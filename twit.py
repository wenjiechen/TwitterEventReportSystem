# Last edit by Marcos Kohler 4_8_2014
import tweepy
import sys
import csv
import distance
import math
import json

consumer_key = "IvnfDQOf0aVOPJ5Vz7buaQ"
consumer_secret = "2FCLK3EXQNjHyE1qP1rMglOLHOSsRGnC7sNYNZiuI"

access_token_key = "15400274-5IgFzMdT24bzwZLPUsthrtz8GbtucRFy1IGfpnsJe"
access_token_secret = "YzV5zZWuhoojiBkdi5yb5ZnChKOoyshpvvT2ZRphTKUFi"

auth1 = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth1.set_access_token(access_token_key,access_token_secret)

# need this line to access user and followers
api = tweepy.API(auth1)

center = {'lat' : 40.7300, 'long' : -73.9950} 		# Washington Square Park
setTerms = ['party']									# Keywords
setLanguages = ['en']								# Language Filter
collectTrainningData = true
#**********************************************************************************************************************
#**********************************************************************************************************************
# Might need to find a way to search old tweets and not use the streaming api
# for tweet in tweepy.Cursor(api.search,q="beer OR alcohol",rpp=1000,result_type="recent",include_entities=True,lang="en").items():
# print tweet.created_at, tweet.text
#**********************************************************************************************************************
#**********************************************************************************************************************


class StreamListener(tweepy.StreamListener):
	
	def __init__(self):
		super(StreamListener, self).__init__()		# Not sure if needed
		self.tweetCount = 0							# Tweets tracked
		self.tweetThresh = 10						# Tweet tracking limit

	def on_status(self,tweet):
		text = ""
		hashtags = ""
		urls = ""
		user_mentions = ""	
		favs = 0
		retweets = 0
		username = ""
		followers = 0
		
		if (self.tweetCount < self.tweetThresh):
		
			if tweet.coordinates:
				
				d = math.ceil(distance.distance_between(tweet.coordinates["coordinates"][1], tweet.coordinates["coordinates"][0], center["lat"], center["long"]))
				
				if d < 10000:
				
					self.tweetCount += 1
					text = tweet.text
					favs = tweet.favorite_count
					print "Text: " + text + "\n" + "Distance: " + str(d) + " mi" + "\n" + "Fav: " + str(favs) + "\n" + "Retweets: " + str(retweets)

					user = api.get_user(tweet.user.screen_name)
					if user:
						username = user.screen_name
						followers = user.followers_count
						print "User: " + username + "\n" + "Followers: " + str(followers)

					for hashtag in tweet.entities['hashtags']:
						hashtags = hashtags + hashtag['text'] + " "
					if hashtags:
						print "Hashtags: " + hashtags

					for url in tweet.entities['urls']:
						urls = urls + url['expanded_url'] + " "
					if urls:
						print "URLs: " + urls


					print "\n"

					# fileText = str(tweet.created_at) + ".txt"
					# text_file = open(fileText,"w")
					# text_file.write("Text: %s\n" % text.encode('utf-8'))
					# text_file.write("Hashtags: %s\n" % hashtags.encode('utf-8'))
					# text_file.write("Favs: %s\n" % favs)
					# text_file.write("Retweets: %s\n" % retweets)
					# text_file.write("User: %s\n" % username.encode('utf-8'))
					# text_file.write("Followers: %s\n" % followers)
					# text_file.close()

					label = 1 # used for trainning classfilier
					csvText
					if (self.tweetCount == 0):
						if collectTrainningData:
							csvText = "TrainData.csv"
                        else:
                            csvText = "Output.csv"
						with open(csvText,'w') as outfile:
						    writer = csv.writer(outfile)
						    writer.writerow((label,text.encode('utf-8'),hashtags.encode('utf-8'),followers))
					else:
						fd = open(csvText,'a')
						writer = csv.writer(fd)
						writer.writerow((label,text.encode('utf-8'),hashtags.encode('utf-8'),followers))
						fd.close()



		else:
			print("Done Collecting Tweets!\n")
			sys.exit()
	#end on_status

	def on_error(self, status_code):
		print "Error: " + repr(status_code)
		return False
	#end on_error

l = StreamListener()
streamer = tweepy.Stream(auth=auth1,listener=l)
streamer.filter(track=setTerms,languages=setLanguages)