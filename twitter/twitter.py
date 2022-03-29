#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time
import logging

import requests
from requests.exceptions import HTTPError
from requests_oauthlib import OAuth1Session


class TwitterSession(OAuth1Session):
    def __init__(self):
        with open('twitter.json') as f:
            config = json.loads(f.read())
        super().__init__(
            client_key=config['CONSUMER_KEY'], client_secret=config['CONSUMER_SECRET'],
            resource_owner_key=config['ACCESS_TOKEN'], resource_owner_secret=config['ACCESS_SECRET'])

    def get(self, url, **kwarg):
        response = super().get(url, **kwarg)
        while response.status_code == 429:
            logging.info("Rate limit reached. Sleep 60s.")
            time.sleep(60)
            response = super().get(url, **kwarg)
        return response
        # if response.status_code == 200:
        #     return response
        # else:
        #     raise HTTPError(f"Unknown twitter response {response.status_code} with {url} {kwarg}\n{response.text}")

    def post(self, url, **kwarg):
        response = super().post(url, **kwarg)
        while response.status_code == 429:
            logging.info("Rate limit reached. Sleep 60s.")
            time.sleep(60)
            response = super().post(url, **kwarg)
        return response
        # if response.status_code == 200:
        #     return response
        # else:
        #     raise HTTPError(f"Unknown twitter response {response.status_code} with {url} {kwarg}\n{response.text}")
    
    def followers_ids(self, user=None):
        ''' Twitter REST APIs Documentation
        https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-followers-ids
        '''
        assert user is None or isinstance(user, int) or isinstance(user, str),\
            "user expects int or str."

        url = "https://api.twitter.com/1.1/followers/ids.json"
        params = {}
        if isinstance(user, int):
            params.update({'user_id': user})
        if isinstance(user, str):
            params.update({'screen_name': user})
        
        response = self.get(url, params=params)
        return response.json()
    
    def followers_list(self, user=None):
        ''' Twitter REST APIs Documentation
        https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-followers-ids
        '''
        assert user is None or isinstance(user, int) or isinstance(user, str),\
            "user expects int or str."

        url = "https://api.twitter.com/1.1/followers/list.json"
        params = {}
        if isinstance(user, int):
            params.update({'user_id': user})
        if isinstance(user, str):
            params.update({'screen_name': user})
        
        response = self.get(url, params=params)
        return response.json()

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
        return response.json()

    def friend_list(self, user=None, count=5000):
        ''' Twitter REST APIs Documentation
        https://dev.twitter.com/rest/reference/get/friends/ids
        '''
        assert user is None or isinstance(user, int) or isinstance(user, str),\
            "user expects int or str."
        assert isinstance(count, int), "count expects int."

        url = "https://api.twitter.com/1.1/friends/list.json"
        params = {}
        if isinstance(user, int):
            params.update({'user_id': user})
        if isinstance(user, str):
            params.update({'screen_name': user})
        params.update({'count': count})
        
        response = self.get(url, params=params)
        return response.json()

    def users_show(self, user=None):
        ''' Twitter REST APIs Documentation
        https://dev.twitter.com/rest/reference/get/users/show
        '''
        assert user is None or isinstance(user, int) or isinstance(user, str),\
            "user expects int or str."

        url = "https://api.twitter.com/1.1/users/show.json"
        params = {}
        if isinstance(user, int):
            params.update({'user_id': user})
        if isinstance(user, str):
            params.update({'screen_name': user})

        response = self.get(url, params=params)
        return response.json()

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

        response = self.get(url, params=params)
        return response.json()

    def statuses_show(self, id_):
        ''' Twitter REST APIs Documentation
        https://dev.twitter.com/rest/reference/get/statuses/show/%3Aid
        '''
        assert type(id_) == int, "id_ expects int"
        url = "https://api.twitter.com/1.1/statuses/show.json"
        params = {'id': id_}
        response = self.get(url, params=params)
        return response.json()

    def status_url(self, id_):
        data = self.statuses_show(id_)
        return "https://twitter.com/{user[screen_name]}/status/{id}".format(data)