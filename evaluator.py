import json
import data_cleaning_filtering as dcf
from bm25 import main

tweet_list = []

'''
with open('Tweet_temp_tweet2.txt0','r') as f:
	t_list = json.load(f)
tweet_list = t_list
filtered_json = dcf.filter_data(tweet_list)

x = json.loads(filtered_json)

#print filtered_json.encode('utf-8')
text = dcf.set_bm25_data_format(x)
#print text.encode('utf-8')


with open('corpus111.txt','w') as fd:
	fd.write(text.encode('utf-8'))

'''


def set_data(index):
    with open(str(index) + '_temp_tweet.txt', 'r') as f:
        t_list = json.load(f)
    tweet_list = t_list
    filtered_json = dcf.filter_data(tweet_list)

    x = json.loads(filtered_json)
    with open('filtered111.txt', 'w') as fd:
        fd.write(str(x))
    text = dcf.set_bm25_data_format(x)
    # print text

    with open('corpus111.txt', 'w') as fd:
        fd.write(text.encode('utf-8'))

    main.start_bm25()
