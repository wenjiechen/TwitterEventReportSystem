import tweepy
import distance
import math

consumer_key = "IvnfDQOf0aVOPJ5Vz7buaQ"
consumer_secret = "2FCLK3EXQNjHyE1qP1rMglOLHOSsRGnC7sNYNZiuI"

access_token_key = "15400274-5IgFzMdT24bzwZLPUsthrtz8GbtucRFy1IGfpnsJe"
access_token_secret = "YzV5zZWuhoojiBkdi5yb5ZnChKOoyshpvvT2ZRphTKUFi"

auth1 = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth1.set_access_token(access_token_key, access_token_secret)

class StreamListener(tweepy.StreamListener):
  
  def on_status(self, tweet):
    # print str(StreamListener.count) + " " + tweet.user.screen_name + "-  " + tweet.text + "\n"
    if tweet.coordinates:
      # tweet coordinates come in longitude, latitude order for some reason
      d = math.ceil(distance.distance_between(tweet.coordinates["coordinates"][1], tweet.coordinates["coordinates"][0], center["lat"], center["long"]))
      # this makes sure tweets are within 25 miles of center
      if d < 10000:
        print tweet.coordinates
        print tweet.text + "(" + str(d) + " mi)"
        print ""

  def on_error(self, status_code):
    print "Error: " + repr(status_code)
    return False


l = StreamListener()
streamer = tweepy.Stream(auth=auth1, listener=l)
# these are our key words to search for
setTerms = ["yankees", "sunshine", "beer"]
# Washington Square Park
center = {"lat" : 40.7300, "long" : -73.9950}
streamer.filter(track = setTerms)