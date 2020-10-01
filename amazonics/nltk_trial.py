import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze_sentences(sentence):
    '''
    Takes in a string and spits out a dict of sentiments - compound, neg, pos, neu.
    '''
    sid = SentimentIntensityAnalyzer()
    print(sentence)
    ss = sid.polarity_scores(sentence)
    return (ss)

def get_entities(sentence):
    '''
    gets the entities from the sentence.
    '''
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged)
    return entities