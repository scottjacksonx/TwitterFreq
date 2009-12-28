#########
# Project: TwitterFreq
# Author: Scott Jackson
# Last Updated: August 9, 2009
# This program gets a user's tweets, sorts them, and then outputs a graph.
# 
# Usage: From the shell, type
#
#	python TwitterFreq.py username [distribution]
#	
#	username: the name of the user whose tweets you want to analyse.
#	distribution: optional argument, either "daily" or "weekly".
#
# Bugs, TODOs, etc:
#  - awful, hack-y code, little-to-no documentation.
#
# Dependencies:
#  - Python (duh)
#  - python-twitter (http://code.google.com/p/python-twitter/)
#
#########



import twitter # for twitter api
import sys	# for cmd-line args
import datetime # for time stuff

class TwitterFreq:
	"""
	The main class for the application.
	"""
	quit = 0
	
	distribution = "-w"
	twitterName = ""
	tweets = []
	
	weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
	hours = ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00",
			 "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00",
			 "20:00", "21:00", "22:00", "23:00"]
	
	
	def __init__(self):
		self.handleArguments()
		
		if self.quit:
			self.printHelp()
			sys.exit()
			
		self.main()
		
	def main(self):
		buckets = self.makeBuckets()
		
		self.tweets = self.getTweets()
		
		buckets = self.sortStatuses(buckets)
		
		self.printGraph(buckets)
			
		
	def getTweets(self):
		"""
		Gets and returns a user's tweets.
		"""
		max_id = None

		api = twitter.Api()
		
		print "Getting " + self.twitterName + "'s last 200 tweets from Twitter..."

		# get the user's tweets -- the maximum that Twitter will allow is 200.
		tweets = api.GetUserTimeline(user=self.twitterName, count=200)
		return tweets


	def makeBuckets(self):
		"""
		Creates buckets to put tweets in.
		"""
		buckets = {}
		if self.distribution == "-d":
			# make 24 buckets, one per hour
			for i in range(0,24):
				buckets[i] = 0
		elif self.distribution == "-w":
			# make 7 buckets, one per day
			for i in range(0,7):
				buckets[self.weekdays[i]] = 0
		return buckets

	def sortStatuses(self, buckets):
		"""
		Looks at each tweet and puts it into the appropriate bucket.
		"""
		print "Sorting " + self.twitterName + "'s tweets..."
		if self.distribution == "-d":
			for s in self.tweets:
				time = datetime.datetime.fromtimestamp(s.GetCreatedAtInSeconds())
				buckets[time.hour] += 1
		elif self.distribution == "-w":
			for s in self.tweets:
				time = datetime.datetime.fromtimestamp(s.GetCreatedAtInSeconds())
				buckets[self.weekdays[time.weekday()]] += 1
		return buckets

	def printGraph(self, buckets):
		"""
		Prints out a bar graph of tweet counts.
		"""
		print ""
		if self.distribution == "-w":
			for d in self.weekdays:
				print paddedDay(d) + "|" + "=" * buckets[d]
		else:
			for i in range(0,24):
				print self.hours[i] + " " + "|" + "=" * buckets[i]
		print ""
			
	

			
	def handleArguments(self):
		"""
		Parses the command-line arguments given.
		"""
		if len(sys.argv) > 1:
			if sys.argv[1] == "-h" or sys.argv[1] == "-help":
				self.quit = 1
			elif len(sys.argv) == 3:
				# Assume that distribution is first, username is second.
				if sys.argv[1] == "-w" or sys.argv[1] == "-d":
					self.distribution = sys.argv[1]
					self.twitterName = sys.argv[2]
				else:
					self.quit = 1
			elif len(sys.argv) == 2:
				self.twitterName = sys.argv[1]
		else:
			self.quit = 1
	
	def printHelp(self):
		"""
		Prints help for the program.
		"""
		print "Usage:"
		print "    python TwitterFreq.py [distribution] twitterUserName"
		print ""
		print "Arguments:"
		print "    distribution -- optional argument. -d or -w. -d means daily, -w means weekly. If this argument is not present, w is assumed."
		print "    twitterUserName -- the Twitter username of the person."
		print ""
		print "For help, use"
		print "    python TwitterFreq.py -h"
		print ""

def paddedDay(d):
	"""
	prints out a weekday padded out to 11 characters.
	"""
	while len(d) != 11:
		d += " "
	return d


TwitterFreq = TwitterFreq()
