import os
import sys
import json
import re
from pyspark import SparkConf, SparkContext

def clean(tweet):
    text = tweet["text"]
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\&\S+;', '', text)
    text = re.sub(r'\\u[0-9]+', '', text)
    text = re.sub(r'@\S+', '', text)
    tweet["text"] = text.replace('#', '')
    return tweet

def tokenize(tweet):
    import nltk
    # nltk.download('punkt')
    nltk.download('stopwords')
    from nltk import word_tokenize
    from nltk.tokenize import WordPunctTokenizer
    from nltk.corpus import stopwords
    text = tweet["text"]
    tokens = nltk.word_tokenize(text)
    for language in ['english', 'spanish']:
        tokens = filter(lambda token: token and token not in stopwords.words(language), tokens)
    tweet["text"] = " ".join(filter(lambda token: len(token) > 2 and len(token) < 20, tokens))
    return tweet

def stem(tweet):
    tokens = tweet["text"].split(" ")
    from nltk.stem.snowball import SnowballStemmer
    for language in ['english', 'spanish']:
        ss = SnowballStemmer(language)
        tokens = [ss.stem(token.lower()) for token in tokens if token]
    tweet["text"] = " ".join(tokens)
    return tweet

def sameletters(s1, s2):
    s1 = re.sub(r'(.)\1+', r'\1', s1)
    s2 = re.sub(r'(.)\1+', r'\1', s2)
    return s1 == s2

def spell_word(word):
    import enchant
    from nltk.metrics import edit_distance
    dictionary = enchant.Dict('en_US')
    max_dist = 2
    try:
        assert word
        word = re.sub(r'(.)\1+', r'\1\1', str(word))
        if dictionary.check(word):
            return word
        suggestions = sorted(dictionary.suggest(word), key = lambda sug: edit_distance(sug, word) * (0 if sameletters(word, sug) else 1))
        try:
            if edit_distance(suggestions[0], word) <= max_dist:
                return suggestions[0]
        except:
            pass
    except UnicodeEncodeError:
        pass
    except AssertionError:
        pass
    return word


def spell(tweet):
    tokens = tweet["text"].split(" ")
    spelled = [spell_word(token) for token in tokens]
    tweet["text"] = " ".join(spelled)
    return tweet

conf = SparkConf().setAppName("edu.uic.cs.cs594.fakenews.preprocessing.py")
sc = SparkContext(conf = conf)

# load tweets
input_rdd = sc.textFile(sys.argv[1])
structured_rdd = input_rdd.map(lambda string: json.loads(string))

# data cleaning
cleaned_rdd = structured_rdd.map(lambda tweet: clean(tweet))

# tokenizing, short unigram removal, stopwords removal
tokens_rdd = cleaned_rdd.map(lambda tweet: tokenize(tweet))

# stemming
stemmed_rdd = tokens_rdd.map(lambda tweet: stem(tweet))

# spell check
spelled_rdd = stemmed_rdd.map(lambda tweet: spell(tweet))

# output
output_rdd = spelled_rdd.map(lambda tweet: json.dumps(tweet))
output_rdd.saveAsTextFile(sys.argv[1].split("/")[0] + "/output")
