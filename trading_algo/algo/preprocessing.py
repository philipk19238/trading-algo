import sys
sys.path.append('..')

import json
import string
import spacy
import en_core_web_sm
from collections import defaultdict
from scraper.models import WSB, Thread, Comment
from ticker_data.tickers import tickers


nlp = en_core_web_sm.load()


def pretty_print(obj):
    print(json.dumps(obj, indent=2))


def get_daily():
    wsb = WSB()
    daily_threads = wsb.threads(limit=1, sort='top')
    for thread in daily_threads:
        pipeline = AlgoPipeline()
        comments = thread.comments(sort='top', limit=100)
        for comment in comments: 
            if comment and comment[0]:
                pipeline.add(AlgoComment(comment))
        pretty_print(pipeline.process_all())
        

def process_ticker(comment_array):
    res = defaultdict(list)
    for comment in comment_array:
        for word in comment.split():
            word = word.lower()
            if word in tickers:
                res[tickers[word]].append(comment)
    return res


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


class AlgoTextPreprocessor(TextPreprocessor):

    def __init__(self, text):
        super().__init__(text)

    def process(self):
        processed_text = super(AlgoTextPreprocessor, self).process()
        return self._extract_ticker(processed_text)

    def _extract_ticker(self, text):
        res = defaultdict(list)
        for word in text.split():
            if self._is_ticker(word) and word not in res:
                res[word].append(text)
        return res

    def _is_ticker(self, word):
        if word[0] == '$' and len(word) >= 2 and word[1:] in tickers:
            return word
        elif word == word.upper() and word in tickers:
            return word


class AlgoComment(Comment, AlgoTextPreprocessor):

    def __init__(self, comment_chain):
        self.comment_chain = comment_chain
        super(Comment, self).__init__(self.comment_chain)
        super(AlgoTextPreprocessor, self).__init__(self.comment)

    def process(self):
        processed_text = super(AlgoComment, self).process()
        if processed_text:
            for key in processed_text:
                processed_text[key] += self.replies
            return processed_text
        return processed_text


class Pipeline:

    def __init__(self):
        self.pipeline = []

    def add(self, new_data):
        self.pipeline.append(new_data)

    def process_all(self):
        return [data.process() for data in self.pipeline]


class AlgoPipeline(Pipeline):

    def __init__(self):
        super().__init__()

    def process_all(self):
        processed_data = super(AlgoPipeline, self).process_all()
        ticker_dict = defaultdict(list)
        for elem in processed_data: 
            for ticker in elem: 
                if ticker in ticker_dict: 
                    ticker_dict[ticker] += elem.get(ticker)
                else:
                    ticker_dict[ticker] = elem.get(ticker)
        return ticker_dict



get_daily()
