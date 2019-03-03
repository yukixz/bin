#!/usr/bin/env python3

import json
import sys
import traceback
from datetime import datetime

import sqlite3
from requests_oauthlib import OAuth1Session


class Twitter():
    def __init__(self):
        with open('daily.json') as f:
            kwargs = json.loads(f.read())
        self.session = OAuth1Session(
            client_key="",
            client_secret="",
            resource_owner_key="",
            resource_owner_secret="",
        )

    def crawl(self, last_id):
        ''' Crawl new tweet from user timeline.
            :param last_id: last tweet's id in database
            :return list:
        '''
        if type(last_id) != int:
            raise TypeError("arg last_id expects int")
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        params = {
            'count': 200,
            'since_id': last_id,
            'max_id': None,
            'trim_user': True,
            'contributor_details': False,
            'exclude_replies': False,
            'include_rts': True,
        }

        while True:
            response = self.session.get(url, params=params)
            tweets = json.loads(response.text)
            if len(tweets) > 0:
                yield from tweets
                params['max_id'] = tweets[-1]['id'] - 1
            else:
                break


class Database():
    def __init__(self):
        self.connection = sqlite3.connect("twitter.db", isolation_level=None)

    def __del__(self):
        # self.connection.commit()
        self.connection.close()

    def insert(self, tweet):
        try:
            tweet_id = int(tweet['id'])
            user_id = int(tweet['user']['id'])
            text = tweet['text']
            time = str(datetime.strptime(
                tweet['created_at'].replace("+0000", ''), "%c"))
            cursor = self.connection.cursor()
            cursor.execute(
                '''INSERT INTO statuses VALUES (?, ?, ?, ?)''',
                (tweet_id, user_id, text, time))
        except sqlite3.Error as err:
            print("Sqlite error inserting tweet %d" % tweet_id, file=sys.stderr)
            traceback.print_exc()

    def get_last_id(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id FROM statuses ORDER BY id DESC LIMIT 1")
        tweet = cursor.fetchone()
        return tweet[0]


if __name__ == '__main__':
    twitter = Twitter()
    database = Database()

    last_id = database.get_last_id()
    timeline = twitter.crawl(last_id)
    for tweet in timeline:
        database.insert(tweet)
