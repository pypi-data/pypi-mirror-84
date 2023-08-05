import re
import os
import stanza
import spacy_udpipe
from collections import Counter

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
EXTERNAL_DIR = ROOT_DIR+'/external_data'

try:
    nlp_udpipe = spacy_udpipe.load(lang='hy')
except Exception:
    spacy_udpipe.download('hy')
    nlp_udpipe = spacy_udpipe.load(lang='hy')

try:
    nlp_stanza = stanza.Pipeline(use_gpu=False, lang='hy', processors='tokenize, mwt, pos, lemma, depparse')
except Exception:
    stanza.download('hy', processors='tokenize, mwt, pos, lemma, depparse')
    nlp_stanza = stanza.Pipeline(use_gpu=False, lang='hy', processors='tokenize, mwt, pos, lemma, depparse')


def letter_tokenize(text: str):
    return list(re.sub(r'[^\u0561-\u0587\u0531-\u0556]', '', text))


def letters_and_numbers(text: str):
    return list(re.sub(r'[^\d\u0561-\u0587\u0531-\u0556]', '', text))


def remove_non_letters(text: str):
    return re.sub(r'[^\s\u0561-\u0587\u0531-\u0556]', ' ', text)


def sentence_tokenize(text: str):
    doc = nlp_udpipe(text)
    return [x.string for x in list(doc.sents)]


def syllables_counter(text: str):
    c = Counter(text)
    return c["ա"] + c["ե"] + c["է"] + c["ը"] + c["ի"] + c["ո"] + c["և"] + c["օ"]
