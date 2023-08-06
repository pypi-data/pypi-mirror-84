import spacy
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize.punkt import PunktSentenceTokenizer
from spacy.lang import pt


try:
    nltk.corpus.stopwords.words('portuguese')
except LookupError:
    nltk.download('stopwords')
finally:
    STOP_WORDS = pt.STOP_WORDS.union(
        set(nltk.corpus.stopwords.words('portuguese'))
    )

try:
    nltk.word_tokenize('some word')
except LookupError:
    nltk.download('punkt')


SYNONYMS_FILE = 'synonyms.txt'
VOCABULARY_FILE = 'vocabulary.txt'
NAMEDENTITITIES_FILE = 'named_entities.txt'


def get_spacy_nlp(disabled=('ner', 'parser', 'tagger')):
    nlp = spacy.load("pt_core_news_sm", disable=disabled)
    nlp.max_length = 10**9

    return nlp


def get_stemmer():
    return SnowballStemmer("portuguese")


def get_stopwords(stop_words=(), extra_stop_words=()):

    stop_words = set(stop_words) or STOP_WORDS

    if extra_stop_words:
        stop_words |= set(extra_stop_words)

    custom_stop_words = set([
        'nestas', 'nestes', 'nesses', 'nessas', 'daqueles',
        'daquelas', 'destes', 'destas', 'desses', 'dessas',
        'nele', 'nela'
    ])

    stop_words |= custom_stop_words
    stop_words = set(w.lower() for w in stop_words)

    return stop_words


def get_vocabulary(preprocess_fn=str.strip):
    with open(VOCABULARY_FILE) as f:
        vocabulary = set(map(preprocess_fn, f.readlines()))

    return vocabulary


def get_sentence_splitter():
    return PunktSentenceTokenizer()
