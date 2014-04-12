import tweepy
import csv
from nltk.tokenize import wordpunct_tokenize
import re

class TrainRecord:

    def __init__(self,label,message,followers):
        self.label = label
        self.message = message
        self.followers = followers
        self.features_set = {}
        self.hashtags = []

        # get the set of unique words contained in a twitter message
        # get rid of punctuation tokens, numbers, and single letters.
        self.message_words = set(wordpunct_tokenize(self.message.lower()))
        self.message_words = [w for w in self.message_words if re.search('[a-zA-Z]', w) and len(w) > 1]


class TrainingCreator:

    def __init__(self, input_csv):
        self.input_csv = input_csv
        self.records_list = []
        self.word_counts = {}
        self.features_set = {}
        self.nonsense_words = ['and', 'the','http']
        self.import_csv()

    def import_csv(self):
        with open(self.input_csv,'rb') as csvfile:
            for line in csvfile.readlines():
                fields = line.split(',')
                if len(fields) == 3:
                    record = TrainRecord(fields[0],fields[1],fields[2])
                    self.records_list.append(record)

        # get words count in all messages
        for record in self.records_list:
            for word in record.message_words:
                if word in self.word_counts:
                    self.word_counts[word] += 1
                else:
                    self.word_counts[word] = 1

        # eliminate words whose count less than 2
        tmp_word_counts = {}
        for k, v in self.word_counts.items():
            if v > 3 and k not in self.nonsense_words:
                tmp_word_counts[k] = v
        self.word_counts = tmp_word_counts
        print self.word_counts
        print len(self.word_counts)

if __name__=='__main__':
    print 'rank'
    file = 'trainData.csv'
    tc = TrainingCreator(file)
