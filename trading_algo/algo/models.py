import sys
sys.path.append('..')

from scraper import Comment
from nlp_model import TextPreprocessor, Pipeline
from ticker_data.tickers import tickers
from collections import defaultdict



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
        elif word in tickers:
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
