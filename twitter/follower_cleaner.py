#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import logging
from time import sleep
from twitter import TwitterSession

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s - %(message)s",
)

class Cache():
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            os.mkdir(path)
        if not os.path.isdir(path):
            raise OSError(f"{path} is NOT directory.")
    
    def _file_path(self, key):
        return os.path.join(self.path, key)
    
    def set(self, key, val):
        try:
            with open(self._file_path(key), 'w', encoding='utf-8') as f:
                f.write(json.dumps(val, ensure_ascii=False))
        except FileNotFoundError:
            raise
    
    def get(self, key):
        try:
            with open(self._file_path(key), 'r', encoding='utf-8') as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return None


session = TwitterSession()
db = Cache("/tmp/follower_cleaner")

def get(url, params=None):
    while True:
        response = session.get(url, params=params)
        if response.status_code == 429:
            logging.warning(f"429 - Too Many Requests. Wait 60 seconds.")
            sleep(30)
            continue
        return response

def post(url, params=None):
    while True:
        response = session.post(url, params=params)
        if response.status_code == 429:
            logging.warning(f"429 - Too Many Requests. Wait 60 seconds.")
            sleep(30)
            continue
        return response

def fetch_followers():
    followers = {}
    cursor = -1
    while cursor != 0:
        logging.info(f"Fetch followers from {cursor}")
        response = get("https://api.twitter.com/1.1/followers/list.json", params={
            "cursor": cursor,
            "count" : 200,
        })
        data = response.json()
        for user in data.get('users', []):
            followers[user['id_str']] = user
        cursor = data['next_cursor']
    db.set('followers', followers)

def fetch_timelines():
    followers = db.get('followers')
    for fid in followers:
        dbkey = f"timeline-{fid}"
        if db.get(dbkey) is not None:
            continue
        logging.info(f"Fetch timeline for {fid}")
        response = get("https://api.twitter.com/1.1/statuses/user_timeline.json", params={
            "user_id"  : fid,
            "count"    : 200,
            "trim_user": True,
        })
        timeline = response.json()
        # HACK: Fix 401 error of protected users.
        if response.status_code == 401:
            timeline = []
        db.set(dbkey, timeline)

def analyse():
    followers = db.get('followers')
    for fid, user in followers.items():
        ## Dangerous words
        FUCK_WORD = ['🇨🇳', '🇹🇼']
        FUCK_FIELD = ['name', 'description']
        for field in FUCK_FIELD:
            for word in FUCK_WORD:
                if word in user[field]:
                    print(f"WORD: {fid} http://twitter.com/{user['screen_name']} {word}")
        ## Following / Followers
        FOLLOW_THRESHOLD = 20
        if user['friends_count'] / (user['followers_count'] or 1) > FOLLOW_THRESHOLD:
            print(f"FOLLOW: {fid} http://twitter.com/{user['screen_name']} {user['friends_count']} {user['followers_count']}")
        ## Tweets
        if user['statuses_count'] == 0 and not user['protected']:
            print(f"TWEET0: {fid} http://twitter.com/{user['screen_name']}")
        tweets = db.get(f"timeline-{fid}")
        retweet_count = 0
        for tweet in tweets:
            try:
                if "RT @" in tweet['text']:
                    retweet_count += 1
            except:
                print(fid, tweet)
                raise
        if retweet_count > 0 and retweet_count == len(tweets):
            print(f"RETWEET: {fid} http://twitter.com/{user['screen_name']} {retweet_count}")

def remove(ids):
    for fid in ids:
        logging.info(f"Remove follower {fid}")
        post("https://api.twitter.com/1.1/blocks/create.json", params={
            'user_id': fid,
        })
        post("https://api.twitter.com/1.1/blocks/destroy.json", params={
            'user_id': fid,
        })

if __name__ == '__main__':
    fetch_followers()
    fetch_timelines()
    analyse()
