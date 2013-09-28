#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @copyright:	GPL v3
# @author:	Dazzy Ding (dazzyd, @ks_magi)

import os, sys
import getopt
import json, re
from datetime import *


def get_date(str, delta=timedelta(hours=8), 
			MONTH2NUMBER={'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',
						  'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}):
	if str[11:13]>'16':
		return ( datetime.strptime(str, "%a %b %d %H:%M:%S +0000 %Y") + delta ).strftime("%Y-%m-%d")
	else:
		return '-'.join([ str[26:30], MONTH2NUMBER[str[4:7]], str[8:10] ])

def main(index_path, result_path, 
		RE_GB=re.compile( r'^Grailbird\.data\.tweets_\d{4}_\d{2} =' ), 
		RE_PATH=re.compile( r'data/js$' )):
	with open(index_path, 'rb') as f:
		index = json.loads( f.read().replace("var tweet_index =  ", "") )
	tweets_path = RE_PATH.sub( "", os.path.dirname(index_path) )
	count = {}
	
	print "Count Start..."
	for i in index:
		print "* "+i['var_name']
		with open(tweets_path+i['file_name'], 'rb') as f:
			c = f.read()
			tweets = json.loads(RE_GB.sub("", c))
		
		for j in tweets:
			d = get_date(j['created_at'])
			if count.has_key(d):
				count[d]+=1
			else:
				count[d]=1
			
	# Save the result.
	print "Saving result..."
	result = open(result_path, 'w')
	keys = count.keys()
	keys.sort()
	for k in keys:
		result.writelines( str(k) +'\t'+ str(count[k]) +'\n' )

if __name__ == "__main__":
	os.chdir(os.path.dirname(__file__) or '.')
	INDEX = "tweets/data/js/tweet_index.js"
	RESULT = "result.log"
	
	optlist, args = getopt.getopt(sys.argv[1:], 'i:l:')
	for k, v in optlist:
		if k == '-i':
			INDEX = v
			print "INDEX set = " + INDEX + "\n"
		if k == '-l':
			RESULT = v
			print "RESULT set = " + RESULT + "\n"
	
	main(INDEX, RESULT)