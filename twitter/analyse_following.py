#!/usr/bin/env python3

''' Analyse your twitter following's tweet source
    @require `pip3 install requests requests_oauthlib`
    @usage 1. Fill your key in `class Storage`
           2. Run `./analyse_following.py 1>result.txt`
'''


import json
import operator
import re
import sys
import time

import requests
from requests_oauthlib import OAuth1Session


class Storage(object):
    CONSUMER_KEY = "CONSUMER_KEY"
    CONSUMER_SECRET = "CONSUMER_SECRET"
    ACCESS_TOKEN = "ACCESS_TOKEN"
    ACCESS_SECRET = "ACCESS_SECRET"


class Session(OAuth1Session):
    def __init__(self, storage=None):
        if storage is None:
            storage = Storage()
        super().__init__(client_key=storage.CONSUMER_KEY,
                         client_secret=storage.CONSUMER_SECRET,
                         resource_owner_key=storage.ACCESS_TOKEN,
                         resource_owner_secret=storage.ACCESS_SECRET,
                         )

    def get(self, url, **kwarg):
        response = super().get(url, **kwarg)
        while response.status_code == 429:
            print("NOTICE: Rate limit reached. Sleep 120s.", file=sys.stderr)
            time.sleep(120)
            response = super().get(url, **kwarg)

        if response.status_code == 200:
            return response
        else:
            print("ERROR: Unknown response", file=sys.stderr)
            print(url, kwarg, file=sys.stderr)
            print(response.status_code, response.text, file=sys.stderr)
            response = requests.Response()
            response._content = b"{}"
            return response

    def friend_ids(self, user=None, count=5000):
        ''' Twitter REST APIs Documentation
        https://dev.twitter.com/rest/reference/get/friends/ids
        '''
        assert user is None or isinstance(user, int) or isinstance(user, str),\
            "user expects int or str."
        assert isinstance(count, int), "count expects int."

        url = "https://api.twitter.com/1.1/friends/ids.json"
        params = {}
        if isinstance(user, int):
            params.update({'user_id': user})
        if isinstance(user, str):
            params.update({'screen_name': user})
        params.update({'count': count})

        response = self.get(url, params=params)
        return json.loads(response.text)

    def user_timeline(self, user=None, count=200):
        ''' Twitter REST APIs Documentation
        https://dev.twitter.com/rest/reference/get/statuses/user_timeline
        '''
        assert user is None or isinstance(user, int) or isinstance(user, str),\
            "user expects int or str."
        assert isinstance(count, int), "count expects int."

        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        params = {}
        if isinstance(user, int):
            params.update({'user_id': user})
        if isinstance(user, str):
            params.update({'screen_name': user})
        params.update({'count': count})
        params.update({'trim_user ': True})

        response = self.get(url, params=params)
        return json.loads(response.text)


class Analyst(object):
    def __init__(self):
        self.session = Session()
        self.html_pattern = re.compile(r'<[^>]*?>')
        self.summary = {}

    def fetch_following(self):
        result = self.session.friend_ids()
        self.following = result['ids']

        # Raise a warning when following count is larger than 5,000
        if result['next_cursor'] != 0:
            print("WARNING: Count 5,000 following only.", file=sys.stderr)

    def summarize(self, id_, timeline):
        ''' Summarize a user's timeline
            Save result to self.summary[id_]
        '''
        if id_ in self.summary:
            summary = self.summary[id_]
        else:
            summary = {}
        for tweet in timeline:
            source = self.html_pattern.sub('', tweet['source'])
            summary[source] = summary.get(source, 0) + 1
        if summary:
            self.summary[id_] = summary

    def analyse(self):
        ''' Print following users' summary
        '''
        self.fetch_following()
        for id_ in self.following:
            if id_ not in self.summary:
                timeline = self.session.user_timeline(id_)
                self.summarize(id_, timeline)

            print("%-12s: " % id_, end="")
            if id_ not in self.summary:
                print("** No result **")
                continue
            summary = self.summary[id_]
            summary = sorted(summary.items(),
                             key=operator.itemgetter(1),
                             reverse=True)
            length = len(summary)
            if length == 0:
                print("** No result **")
                continue
            if length > 4:
                length = 4
            for i in range(length - 1):
                print("%-22s %2d | " % summary[i], end="")
            print("%-22s %2d" % summary[length - 1])


if __name__ == '__main__':
    analyst = Analyst()
    analyst.analyse()
