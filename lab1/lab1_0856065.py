# -*- coding: utf-8 -*-
"""lab1-0856065.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cJu87ZYzkJJK26UQLuOjsxnClmclxBbY

## Fetching the corpus
"""

import pandas as pd
import math
import string

def get_corpus():
  df = pd.read_csv("https://raw.githubusercontent.com/bshmueli/108-nlp/master/reuters.csv")
  print("Dataset size", len(df))
  print("Dataset columns", df.columns)
  titles = df['title'].to_list() # remember to revert
  contents = df['content'].to_list()
  return titles, contents

def tokenize(document):
  words = document.split(' ')
  return words

"""## Computing word frequencies"""

from collections import Counter

def get_vocab(corpus):
  vocabulary = Counter()
  for document in corpus:
    # Turn to lowercase
    d_lower = document.lower()

    # Remove punctuation
    remove_punctuation_map = dict((ord(char), None) for char in (string.punctuation+"”"))
    no_punctuation = d_lower.translate(remove_punctuation_map)
    
    # Tokenize
    tokens = tokenize(no_punctuation)
    
    # Filter stopwords and numbers and remove ""
    sw = pd.read_csv("https://raw.githubusercontent.com/bshmueli/108-nlp/master/stopwords.txt", header=None)
    sw = sw.values
    filtered = [w for w in tokens if (not w in sw) and (not w == "") and (not w.isdigit())]
    
    vocabulary.update(filtered)
  return vocabulary

def get_doc_vocab(document):
  vocabulary = Counter()
  # Turn to lowercase
  d_lower = document.lower()

  # Remove punctuation
  remove_punctuation_map = dict((ord(char), None) for char in (string.punctuation+"”"))
  no_punctuation = d_lower.translate(remove_punctuation_map)
    
  # Tokenize
  tokens = tokenize(no_punctuation)
    
  # Filter stopwords and numbers and remove ""
  sw = pd.read_csv("https://raw.githubusercontent.com/bshmueli/108-nlp/master/stopwords.txt", header=None)
  sw = sw.values
  filtered = [w for w in tokens if (not w in sw) and (not w == "") and (not w.isdigit())]
    
  vocabulary.update(filtered)
  return vocabulary

"""## Computing TFIDF vector"""

def TF(word, doc_vocab): # the frequency of term x in document y
  return doc_vocab[word] / sum(doc_vocab.values())

def DF(word, vocab): # number of documents contains x
  return sum(1 for count in vocab if word in count)

def IDF(word, vocab):
  return math.log(len(vocab) / DF(word, vocab))

def TFIDF(word, doc_vocab, vocab):
  return TF(word, doc_vocab) * IDF(word, vocab)

def doc2vec(doc):
  doc_vocab = get_doc_vocab(doc)
  words = list(doc_vocab)
  return [TFIDF(token, doc_vocab, vocab) if token in words else 0 for token, freq in vocab]

"""## Computing the similarity between two documents"""

def cosine_similarity(vec_a, vec_b):
  assert len(vec_a) == len(vec_b)
  if sum(vec_a) == 0 or sum(vec_b) == 0:
    return 0 # hack
  a_b = sum(i[0] * i[1] for i in zip(vec_a, vec_b))
  a_2 = sum([i*i for i in vec_a])
  b_2 = sum([i*i for i in vec_b])
  return a_b/(math.sqrt(a_2) * math.sqrt(b_2))

def doc_similarity(doc_a, doc_b):
  return cosine_similarity(doc2vec(doc_a), doc2vec(doc_b))

"""## Find similar documents"""

def k_similar(seed_id, k=5):
  seed_doc = corpus[seed_id]
  print('> "{}"'.format(titles[seed_id]))

  similarities = [doc_similarity(seed_doc, doc) for doc in corpus]
  top_indices = sorted(range(len(similarities)), key=lambda i: similarities[i])[-k:]
  nearest = [[titles[id], similarities[id]] for id in top_indices]
  for story in reversed(nearest):
    print('* "{}" ({})'.format(story[0], story[1]))

"""## Test our program"""

titles, corpus = get_corpus()
vocab = get_vocab(corpus).most_common(1000)
k_similar(856065%1000)