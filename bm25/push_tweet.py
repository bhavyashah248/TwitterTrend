import requests
import pprint
import json
import os


def can_push(i):
	#print "we are in can push"
	ff = 'bm25/can_push/'+str(i)+'.txt'
	if os.path.exists(ff) and os.path.getsize(ff) > 0:		
		with open(ff,'r') as f:
			num = int(f.readline())

		f = open(ff,'w')
		if num < 10:
			num += 1
			f.write(str(num))
			f.close()
			return True
		else:
			f.write('11')
			f.close()		
			return False


	else:
		f = open(ff,'w')
		f.write('0')
		f.close()
		return True


def lets_push(query_id, tweet_id, client_id, i):
	cpush = can_push(i)
	if cpush:
		url = 'http://54.164.151.19/tweet/{}/{}/{}'.format(query_id, tweet_id, client_id)
		headers = {'Content-type': 'application/json'}
		response = requests.post(url, headers=headers)
	#	pprint.pprint(response)
	#	pprint.pprint(response.status_code)
		
		print "------------------------------------------ We have got results hurraaah----------------------------"
		if response.status_code == 204:
			print query_id+" posted"
	else:
		print "query id %s is greter than 10" %(i)

if __name__ == '__main__':
	lets_push('MB226', '738418531520352258', 'Eqnn7Hu7bSyd',5)


def get_query_id(i):
	#print "we are in get_query_id"
	with open('bm25/tweet_id-num.txt','r') as f:
		for line in f:
			key = line.split(',')
			if i == int(key[0]):
				return key[0]
			else:
				pass


def get_tweet_id(s):
	word = s.split(',')
	return word[0]

