from collections import deque
from functools import lru_cache
import json

from .api import reddit


class WSB:
    BASE = "https://oauth.reddit.com/r/wallstreetbets/"

    def threads(self, sort="new", name=None, limit=25):
        threads = {}
        endpoint = self.BASE + f"{sort}.json?limit={limit}"
        r = reddit.get(endpoint)
        for thread_obj in r.json().get("data").get("children"):
            thread = thread_obj.get("data")
            title = thread.get("title")
            id = thread.get("id")
            permalink = thread.get("permalink")
            threads[title] = Thread(title=title, permalink=permalink, id=id)
        if name:
            return threads[name]
        return list(threads.values())

    def daily_threads(self, sort="new", name=None, limit=25):
        threads = {}
        endpoint = (
            self.BASE
            + 'search.json?q=flair_name%3A"Daily%20Discussion"&restrict_sr=1'
            + f"&limit={limit}&sort={sort}"
        )
        r = reddit.get(endpoint)
        for thread_obj in r.json().get("data").get("children"):
            thread = thread_obj.get("data")
            title = thread.get("title")
            id = thread.get("id")
            permalink = thread.get("permalink")
            threads[title] = Thread(title=title, permalink=permalink, id=id)
        if name:
            return threads[name]
        return list(threads.values())


class Thread:
    BASE = "https://oauth.reddit.com"

    def __init__(self, title, permalink, id):
        self.title = title
        self.link = permalink
        self.id = id

    def __repr__(self):
        return json.dumps(self.__dict__)

    def _dfs(self, root):
        res, stack = [], []
        stack.append(root)
        while stack:
            curr = stack.pop().get("data")
            res.append(curr.get("body"))
            if curr.get("replies"):
                for reply in curr.get("replies").get("data").get("children"):
                    stack += [reply] if reply else []
        return res

    def comments(self, limit=25, sort="new"):
        endpoint = self.BASE + self.link + f"?limit={limit}&sort={sort}"
        r = reddit.get(self.BASE + self.link)
        response = r.json()
        main, comments = response[0], response[1]
        res = []
        for comment in comments.get("data").get("children"):
            res.append(self._dfs(comment))
        return res


class Comment:
    def __init__(self, comment_chain):
        self.comment_chain = comment_chain

    def __repr__(self):
        return json.dumps({"comment": self.comment, "replies": self.replies})

    @property
    def comment(self):
        return self.comment_chain[0]

    @property
    @lru_cache()
    def replies(self):
        if self.comment_chain == 1: 
            return []
        return self.comment_chain[1:]

if __name__ == '__main__':
    wsb = WSB()
    res = []
    threads = wsb.daily_threads(sort='new', limit=100)
    for thread in threads:
        comments = thread.comments(sort="top", limit=100)
        for comment in comments:
            all_comments = [comment.comment] + comment.replies
            for elem in all_comments:
                res.append(
                    {'body':elem}
                )
    with open('daily_data.json', 'w') as f: 
        json.dump(res, f)
