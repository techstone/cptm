"""Script that generates a (synthetic) corpus to test the CPT model.

The corpus consists of 5 documents containing fixed topics and opinions.

The generation process is described in the CPT paper.

A text document contains the topic words on the first line and the opion words
on the second line.

Usage: python generateCPTCorpus.py <out dir>
"""
import argparse
import numpy as np
from collections import Counter
import codecs
import os


parser = argparse.ArgumentParser()
#parser.add_argument('num_doc', help='the number of documents to be generated')
#parser.add_argument('num_topic_words', help='the number of topic words per '
#                    'document')
#parser.add_argument('num_opinion_words', help='the number of opinion words '
#                    'per document')
parser.add_argument('out_dir', help='the directory where the generated '
                    'documents should be saved.')
args = parser.parse_args()

if not os.path.exists(args.out_dir):
    os.makedirs(args.out_dir)

topic_vocabulary = np.array(['zon',
                             'ijs',
                             'strand',
                             'vanille',
                             'chocola',
                             'broccoli',
                             'wortel'])
opinion_vocabulary = np.array(['warm',
                               'zwemmen',
                               'zonnig',
                               'bewolkt',
                               'vies',
                               'lekker',
                               'koud'])

real_theta_topic = np.array([[1.0, 0.0, 0.0],
                             [0.0, 1.0, 0.0],
                             [0.0, 0.0, 1.0],
                             [0.5, 0.5, 0.0],
                             [0.0, 0.5, 0.5]])
real_phi_topic = np.array([[0.4, 0.2, 0.4, 0.0, 0.0, 0.0, 0.0],
                           [0.0, 0.3, 0.0, 0.35, 0.35, 0.0, 0.0],
                           [0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.5]])
real_phi_opinion = np.array([[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                             [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                             [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]])

num_topics = real_theta_topic.shape[1]
length_topic = 50
length_opinion = 20

for m, tm in enumerate(real_theta_topic):
    out_file = os.path.join(args.out_dir, 'document{}.txt'.format(m+1))
    print out_file
    with codecs.open(out_file, 'wb', 'utf8') as f:
        topic_words = []
        topic_counter = Counter()
        for i in range(length_topic):
            # topic words
            topic = np.random.multinomial(1, tm).argmax()
            topic_counter[topic] += 1
            word = np.random.multinomial(1, real_phi_topic[topic]).argmax()
            topic_words.append(topic_vocabulary[word])
        #print topic_counter
        f.write('{}\n'.format(' '.join(topic_words)))

        opinion_words = []
        # select opinion (index) based on topic occurrence
        om = np.array([float(topic_counter[i]) for i in range(num_topics)])
        #print om
        # normalize
        om /= sum(om)
        for i in range(length_opinion):
            # opinion words
            topic = np.random.multinomial(1, om).argmax()
            word = np.random.multinomial(1, real_phi_opinion[topic]).argmax()
            opinion_words.append(opinion_vocabulary[word])
        f.write(' '.join(opinion_words))