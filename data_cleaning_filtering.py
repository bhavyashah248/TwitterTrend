import json
import re
from nltk.stem import WordNetLemmatizer

'''
text = " #scFine #@thFn,#gdklj @chin :chint ?cs	 https://www.google.com?name=123&vale=ad google *&hj&" 
ree = re.sub(r'#'," ",text)
ree = ree.lower()
ree = re.sub(r'https\S+',' ', ree)
ree = re.sub(r"(?:\@|https?\://)\S+", "", ree)
ree = re.sub(r'[^a-zA-Z0-9]',' ',ree)
print ree
'''


def clean_tweet_data(text):
    ree = re.sub(r'#', " ", text)
    ree = re.sub(r' us ', "", ree)
    ree = ree.lower()
    ree = re.sub(r'@', " ", ree)
    ree = re.sub(r'-', " ", ree)
    ree = re.sub(r"(?:\@|https?\://)\S+", "", ree)
    # ree = re.sub(r'https\S+',' ', ree)
    ree = re.sub(r'[^a-zA-Z]', ' ', ree)
    ree = re.sub(r' +', ' ', ree)
    return ree


#	print ree.encode('utf-8')

def do_lemmatize(sentence):
    wnl = WordNetLemmatizer()
    line = sentence.split()
    w = []
    for word in line:
        w.append(wnl.lemmatize(word))

    s = ' '.join(w)
    return s


def filter_data(json_data):
    response = []
    for tweet in json_data:
        tweet = tweet.strip()
        # data = json.loads(tweet.decode('string-escape').strip('"'))
        data = json.loads(tweet)

        t_id = data['id']
        text = data['text']
        text = clean_tweet_data(text)
        text = do_lemmatize(text)
        timestamp = data['timestamp_ms']
        try:
            if data['retweeted_status']:
                retweeted = True
        except:
            retweeted = False
        fav_count = data['favorite_count']
        user_followers = data['user']['followers_count']
        if retweeted == True:
            continue
        else:
            text_2_word = text.split()

            if len(text_2_word) > 4:
                # print text
                # print str(len(text))+" : "+str(len(text_2_word))
                response.append({'id': t_id, 'text': text, 'timestamp_ms': timestamp, 'retweeted': retweeted,
                                 'fav_count': fav_count, 'user_followers': user_followers})
            else:
                # print text
                continue

    res_json = json.dumps(response)
    #	print str(response)
    return res_json


def set_bm25_data_format(json_data):
    all_text = ""
    for tweet in json_data:
        #		print tweet
        #		data = json.loads(tweet)
        data = tweet
        # uncomment above  line latter
        # data = json.loads(tweet)
        t_id = data['id']
        text = data['text']

        all_text += "$$$" + str(t_id) + " \n" + text + " \n"
    #print all_text
    return all_text
