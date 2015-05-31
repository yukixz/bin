#!/usr/bin/env python3

import json
from datetime import datetime

import pymysql
from requests_oauthlib import OAuth1Session


class Twitter():
    def __init__(self):
        self.session = OAuth1Session(
            client_key="{consumer_key}",
            client_secret="{consumer_secret}",
            resource_owner_key="{access_token}",
            resource_owner_secret="{access_secret}",
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
        self.connection = pymysql.connect(
            host="localhost",
            user="{mysql_user}",
            password="{mysql_password}",
            database="twitter",
            charset="utf8mb4",
            )

    def insert(self, tweet):
        try:
            tweet_id = tweet['id']
            user_id = tweet['user']['id']
            text = tweet['text']
            time = str(datetime.strptime(
                tweet['created_at'].replace("+0000", ''), "%c"))
            cursor = self.connection.cursor()
            cursor.execute(
                '''INSERT INTO statuses VALUES (%s, %s, %s, %s)''',
                (tweet_id, user_id, text, time))
        except pymysql.err.ProgrammingError as err:
            print("Fail to insert tweet: %d" % tweet_id, file=sys.stderr)
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
