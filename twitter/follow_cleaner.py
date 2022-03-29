#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import json
import logging
from datetime import datetime
from twitter import TwitterSession

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


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s - %(message)s",
)
session = TwitterSession()
db = Cache("/tmp/follow_cleaner")


def fetch_following():
    if db.get('following') is None:
        following = {}
        cursor = -1
        while cursor != 0:
            logging.info(f"Fetch following from {cursor}")
            response = session.get("https://api.twitter.com/1.1/friends/list.json", params={
                "cursor": cursor,
                "count" : 200,
            })
            data = response.json()
            for user in data.get('users', []):
                following[user['id_str']] = user
            cursor = data['next_cursor']
        db.set('following', following)
    return db.get('following')

def fetch_followers():
    if db.get('followers') is None:
        followers = {}
        cursor = -1
        while cursor != 0:
            logging.info(f"Fetch followers from {cursor}")
            response = session.get("https://api.twitter.com/1.1/followers/list.json", params={
                "cursor": cursor,
                "count" : 200,
            })
            data = response.json()
            for user in data.get('users', []):
                followers[user['id_str']] = user
            cursor = data['next_cursor']
        db.set('followers', followers)
    return db.get('followers')

def fetch_timelines(followers):
    for fid in followers:
        dbkey = f"timeline-{fid}"
        if db.get(dbkey) is not None:
            continue
        logging.info(f"Fetch timeline for {fid}")
        response = session.get("https://api.twitter.com/1.1/statuses/user_timeline.json", params={
            "user_id"  : fid,
            "count"    : 200,
            "trim_user": True,
        })
        timeline = response.json()
        # HACK: Fix 401 error of protected users.
        if response.status_code == 401:
            timeline = []
        db.set(dbkey, timeline)
    

def analyse_following(following):
    for fid, user in following.items():
        tweets = db.get(f"timeline-{fid}")
        last_time = datetime(year=1970, month=1, day=1)
        sources = {}
        for tweet in tweets:
            tweet_time = datetime.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
            if tweet_time > last_time:
                last_time = tweet_time
            tweet_source = tweet['source']
            if tweet_source not in sources:
                sources[tweet_source] = 0
            sources[tweet_source] += 1
        
        # now = datetime.now()
        # if last_time <= (now - timedelta(days=400)):
        #     print(fid.ljust(20), f"TIME http://twitter.com/{user['screen_name']} {last_time}")
        sources_list = list(sources.items())
        sources_list.sort(key=lambda x: x[1], reverse=True)
        to_print = True
        for [s, n] in sources_list:
            if 'Twitter' in s or 'Tweetbot' in s:
                to_print = False
        if to_print:
            print(fid.ljust(20), f"http://twitter.com/{user['screen_name']}")
            for [s, n] in sources_list:
                m = re.match(r'<a.+?>(.+)</a>', s)
                s = m.group(1)
                print(''.ljust(20), str(n).ljust(3), s)

def analyse_followers(followers, following={}):
    for fid, user in followers.items():
        if fid in following:
            continue
        bads = []
        ## Bad words
        BAD_WORDS = ['🇨🇳', '🇹🇼']
        BAD_FIELDS = ['name']
        for field in BAD_FIELDS:
            for word in BAD_WORDS:
                if word in user[field]:
                    bads.append(f"WORD:{word}")
        ## Following / Followers
        FOLLOW_THRESHOLD = 20
        if user['friends_count'] / (user['followers_count'] or 1) > FOLLOW_THRESHOLD:
            bads.append(f"FOLLOW:{user['friends_count']}/{user['followers_count']}")
        ## Tweets
        if user['statuses_count'] == 0 and not user['protected']:
            bads.append(f"TWEET:0")
        ## Retweet
        tweets = db.get(f"timeline-{fid}")
        retweet_count = 0
        for tweet in tweets:
            try:
                if "RT @" in tweet['text']:
                    retweet_count += 1
            except:
                print(fid, tweet)
                raise
        if retweet_count >= 10 and retweet_count == len(tweets):
            bads.append(f"RETWEET:{retweet_count}")
        # Output
        if len(bads) >= 1:
            print(user['id_str'].ljust(20), f"http://twitter.com/{user['screen_name']}".ljust(35), ' '.join(bads))
            yield fid

def remove_following(ids):
    for fid in ids:
        logging.info(f"Remove following {fid}")
        session.post("https://api.twitter.com/1.1/friendships/destroy.json", params={
            'user_id': fid,
        })

def remove_followers(ids):
    for fid in ids:
        logging.info(f"Remove follower {fid}")
        session.post("https://api.twitter.com/1.1/blocks/create.json", params={
            'user_id': fid,
        })
        session.post("https://api.twitter.com/1.1/blocks/destroy.json", params={
            'user_id': fid,
        })


if __name__ == '__main__':
    following = fetch_following()
    followers = fetch_followers()
    ids = followers
    fetch_timelines(ids)
    bids = analyse_followers(followers, following)
    # remove_followers(bids)
