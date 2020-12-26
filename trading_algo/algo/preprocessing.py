from models import AlgoComment, AlgoPipeline
from scraper import WSB
import json 

def pretty_print(obj):
    print(json.dumps(obj, indent=2))


def get_daily():
    wsb = WSB()
    daily_threads = wsb.threads(limit=10, sort='top')
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






get_daily()
