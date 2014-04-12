from nltk.tokenize import wordpunct_tokenize
import re

class Record:

    def __init__(self,label,message,followers):
        self.label = label
        self.message = message
        self.followers = followers
        self.features_set = {}
        self.hashtags = []
        self.probability = 0
        # get the set of unique words contained in a twitter message
        # get rid of punctuation tokens, numbers, and single letters.
        self.message_words = set(wordpunct_tokenize(self.message.lower()))
        self.message_words = [w for w in self.message_words if re.search('[a-zA-Z]', w) and len(w) > 1]

    # generate message's features_set according to input features
    def get_features_set(self,features_set):
        for k,v in features_set.items():
            if k in self.message_words:
                self.features_set[k] = 1
            else:
                self.features_set[k] = 0


class Ranker:

    def __init__(self, training_data_csv, min_len, min_frequencey):
        self.training_data_csv = training_data_csv
        self.features_set = {}
        self.min_len = min_len
        self.min_frequency = min_frequencey
        self.nonsense_words = ['and', 'the','http']
        self.training_data = []

    def construct_training_data(self):
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

        # construct feature set for evey record
        for record in records_list:
            record.get_features_set(self.features_set)
            # create training data for NLP model
            self.training_data.append((record.features_set,record.label))



if __name__=='__main__':
    trainingfile = 'trainData.csv'
    min_len = 1
    min_frequency = 3
    tc = Ranker(trainingfile,min_len,min_frequency)
    tc.construct_training_data()
    print tc.training_data