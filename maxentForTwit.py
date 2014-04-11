import nltk

train = [
     (dict(sunny=1,rainy=1,windy=1), 'sport'),
     (dict(sunny=1,rainy=1,windy=1), 'weather'),
     (dict(sunny=1,rainy=1,windy=0), 'others'),
     (dict(sunny=0,rainy=1,windy=1), 'weather'),
     (dict(sunny=0,rainy=1,windy=1), 'sport'),
     (dict(sunny=0,rainy=0,windy=1), 'others'),
     (dict(sunny=0,rainy=1,windy=0), 'weather'),
     (dict(sunny=0,rainy=0,windy=0), 'weather'),
     (dict(sunny=0,rainy=1,windy=1), 'others'),
     ]
     
test = [
     (dict(sunny=1,rainy=0,windy=1)), # unseen
     (dict(sunny=1,rainy=0,windy=0)), # unseen
     (dict(sunny=0,rainy=1,windy=1)), # seen 3 times, labels=y,y,x
     (dict(sunny=0,rainy=1,windy=0)), # seen 1 time, label=x
     ]

def NaiveBayesClassifier():
	classifier = nltk.classify.NaiveBayesClassifier.train(train)
	print sorted(classifier.labels())
	print classifier.batch_classify(test)
	print 'prob(x) prob(y)'
	for pdist in classifier.batch_prob_classify(test):
		print "%.4f %.4f" %(pdist.prob('weather'), pdist.prob('others'))
	# classifier.show_most_informative_features()	

def print_maxent_test_header():
	print ' '*11+''.join(['      test[%s]  ' % i for i in range(len(test))])
	print ' '*11+'     p(x)  p(y)'*len(test)
	print '-'*(11+15*len(test))

def test_maxent(algorithm):
	print '%1ls' %algorithm,
	try:
		classifier = nltk.classify.MaxentClassifier.train(
			train, algorithm, trace = 0, max_iter=100)
	except Exception as e:
		print 'Error: %r' %e
		return
	for featureset in test:
		pdist = classifier.prob_classify(featureset)
		print '%8.2f %6.2f' %(pdist.prob('weather'),pdist.prob('others')),
	print ''
	
def main():
	print '----NaiveBayesClassifier----'
	NaiveBayesClassifier()
	print '----Maximum Entropy classifier----'
	print_maxent_test_header()
	test_maxent('GIS')
	test_maxent('IIS')

if __name__ == '__main__':
	main()