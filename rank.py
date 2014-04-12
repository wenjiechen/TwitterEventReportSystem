from nltk.tokenize import wordpunct_tokenize
import re
import nltk

class Record:

    def __init__(self,label,message,followers):
        """
            a twitter message's model for calculating its impact score
        :param label: used for classify
        :param message: twitter message text
        :param followers: twitter account's followers
        """
        self.label = label
        self.message = message
        self.followers = followers
        self.features_set = {}      # used by classifier
        self.hashtags = []          # words marked by hashtags
        self.probability = 0.0        # relevance to the label '1'
        self.impact_score = 0.0       # = probability * (followers+1)
        # get the set of unique words contained in a twitter message
        self.message_words = set(wordpunct_tokenize(self.message.lower()))
        # get rid of punctuation tokens, numbers, and single letters.
        self.message_words = [w for w in self.message_words if re.search('[a-zA-Z]', w) and len(w) > 1]

    # generate a twitter message's features_set according to input features
    def get_features_set(self,features_set):
        for k,v in features_set.items():
            if k in self.message_words:
                self.features_set[k] = 1
            else:
                self.features_set[k] = 0

class Ranker:

    def __init__(self, training_data_csv, test_data_csv, min_len=1, min_frequency=3,topNum=5):
        """
            Classify twitter message in test data file and calculate their impact scores
        :param training_data_csv:
        :param test_data_csv:
        :param min_len:
        :param min_frequency:
        :param topNum:
        """
        self.training_data_csv = training_data_csv
        self.test_data_csv = test_data_csv
        self.features_set = {}              # generate from training data, unique words to indicate a specific event
        self.training_data = []             # generate from training_data_csv file, each twitter message is a training record
        self.classified_records_list = []   # classified twitter records
        self.topN_records = []              # records having the top N impact score
        self.topNum = topNum                # the length of topN_records list
        self.nonsense_words = ['and', 'the','http','co']    # nonsense words needed to be eliminated from features_set
        self.min_len = min_len              # the length of words in features_set are grater than min_len
        self.min_frequency = min_frequency  # the frequency of words in features_set are greater than min_frequency

    # from input training file, create words in features_set and training_data list
    def __construct_training_data(self):
        records_list = []
        word_counts= {}
        # read csv file, create records list
        with open(self.training_data_csv,'rb') as csvfile:
            for line in csvfile.readlines():
                fields = line.split(',')
                if len(fields) == 3:
                    record = Record(fields[0],fields[1],fields[2])
                    records_list.append(record)

        # get words count in all messages
        for record in records_list:
            for word in record.message_words:
                if word in word_counts:
                    word_counts[word] += 1
                else:
                    word_counts[word] = 1

        # eliminate words whose count less than min frequency
        for k, v in word_counts.items():
            if v > self.min_frequency and k not in self.nonsense_words:
                self.features_set[k] = v

        # create training data for NLP model
        for record in records_list:
            # construct feature set for evey record
            record.get_features_set(self.features_set)
            self.training_data.append((record.features_set,record.label))

    # use maximum entropy classify a twitter to different events set
    # Here we only have two events : 1 or 0
    # event 1 means the twitter message talks about we specified topic
    # event 0 means the twitter message talks about other events
    # probability of event 1 + probability of event 0 = 1
    def __get_classify_probability(self,records_list,algorithm='GIS'):
        try:
            classifier = nltk.classify.MaxentClassifier.train(
			self.training_data, algorithm, trace = 0, max_iter=100)
        except Exception as e:
            print 'Error: %r' %e
            return

        for record in records_list:
            probability = classifier.prob_classify(record.features_set)
            record.probability = probability.prob('1')
            # print record.message
            # print '%6.2f, %6.2f' %(probability.prob('1'),probability.prob('0'))
        self.classified_records_list = records_list

    # calculate impact scores of twitter messages in test data
    # generate classified_records_list and topN_records
    def score_test_data(self):
        self.__construct_training_data()

        # read csv file, create records list
        records_list = []
        with open(self.test_data_csv,'rb') as csvfile:
            for line in csvfile.readlines():
                fields = line.split(',')
                if len(fields) == 3:
                    record = Record(fields[0],fields[1],fields[2])
                    record.get_features_set(self.features_set)
                    records_list.append(record)

        # classify twitter messages and get their probability distance for different labels
        self.__get_classify_probability(records_list)
        records_list = sorted(records_list[:], key=lambda record : record.probability,reverse=True)
        for r in records_list:
            r.impact_score = r.probability * (float(r.followers)+1)
        self.classified_records_list = records_list

        # get topN impact score record
        topN = []
        for i in range(0,self.topNum):
            if i < len(records_list):
                topN.append(records_list[i])
                # print topN[i].impact_score

        self.topN_records = topN

    # demonstrate getting top 5 messages related to event 1
    def demo_print_topN_message(self):
        ranker.score_test_data()
        print 'top ',topNum,' impact score twitter messages are: '
        for r in ranker.topN_records:
            print r.message
            print 'impact score: ', r.impact_score

if __name__=='__main__':
    training_data_csv = 'trainData_topic_party.csv'
    test_data_csv = 'testData_topics_beer_party.csv'
    min_len = 1
    min_frequency = 3
    topNum = 5
    ranker = Ranker(training_data_csv,test_data_csv,topNum=topNum)
    ranker.demo_print_topN_message()