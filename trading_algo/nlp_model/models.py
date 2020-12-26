import string
import spacy
import en_core_web_sm
from collections import defaultdict

nlp = en_core_web_sm.load()


class TextPreprocessor:

    def __init__(self, text):
        self.text = text

    def process(self):
        doc = nlp(self.text)
        removed_punct = self._remove_punct(doc)
        removed_stop_words = self._remove_stop_words(removed_punct)
        return self._lemmatize(removed_stop_words)

    def _remove_punct(self, doc):
        return [t for t in doc if t.text not in string.punctuation]

    def _remove_stop_words(self, doc):
        return [t for t in doc if not t.is_stop]

    def _lemmatize(self, doc):
        return ' '.join([t.lemma_ for t in doc])


class Pipeline:

    def __init__(self):
        self.pipeline = []

    def add(self, new_data):
        self.pipeline.append(new_data)

    def process_all(self):
        return [data.process() for data in self.pipeline]
