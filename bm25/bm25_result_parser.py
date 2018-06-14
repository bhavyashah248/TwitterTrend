import numpy as np
import os
from push import push_tweet
import test_jaccard as tc
from push_tweet import *


# function will take file as input and create files as per query id in query folder.
def seperate_store_result():
    with open('ss_bm25_output.txt', 'r') as f:
        for line in f:
            # print str(line)
            word = line.split(',')
            query_no = word[0]
            if len(word) == 5:
                with open('bm25/query/' + query_no + '.txt', 'a') as wf:
                    # print query_no+" "+str(word)
                    wf.write(word[1] + ", " + word[2] + ", " + word[3] + ", " + word[4])
            else:
                pass


def sort_file_result(query_size):
    i = 1
    while i < query_size:
        try:
            data = []
            with open('bm25/query/' + str(i) + '_relevent.txt', 'r') as inf:
                for line in inf:
                    line = line.split(',')
                    data.append(line)
            with open('bm25/query/' + str(i) + '_relevent_sorted.txt', 'w') as of:
                m = sorted(data, key=lambda data_entry: float(data_entry[2]), reverse=True)
                np.savetxt(of, m, fmt='%s', delimiter=',', newline='')
            # of.write(str(m))
        except:
            pass
        # print "Not processed query line :"+str(i)
        i += 1


def seperate_relevent_tweet(val_thresold, query_size):
    i = 1
    while i < query_size:
        data = []
        try:
            with open('bm25/query/' + str(i) + '.txt', 'r') as inf:
                out_file = open('bm25/query/' + str(i) + '_relevent.txt', 'w')
                for line in inf:
                    word = line.split(',')
                    if float(word[2]) > val_thresold:
                        out_file.write(line)
                    else:
                        continue
                out_file.close()
        except:
            pass
        # print "seperate_relevent_tweet Error :"+str(i)
        i += 1


def save_files(query_size):
    i = 1
    while i < query_size:
        try:
            data = []
            with open('bm25/query/' + str(i) + '.txt', 'r') as inf:
                of = open('bm25/query/end_of_day/' + str(i) + '_all_day.txt', 'a')
                for line in inf:
                    of.write(line)
                of.close()
        except:
            pass
        # print "Not saved query number:"+str(i)
        i += 1


def calculate_jaccard(jaccard_thresold, query_size):
    # print "we r in calculate_jaccard"
    i = 1
    first_time_flag = 0
    while i < query_size:
        data = []
        try:
            print "we r in calculate_jaccard"
            in_path = 'bm25/query/' + str(i) + '_relevent_sorted.txt'
            with open(in_path, 'r') as inf:
                # print os.getcwd()
                full_path = os.getcwd()
                out_path = full_path + '/bm25/query/' + str(i) + '_pushed.txt'
                # print out_path
                # print "lets check if file exists"+ str(os.path.exists(out_path)) +" :"+ str(os.path.getsize(out_path) > 0)
                if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                    print "before opening file"
                    out_file = open(out_path, 'r')
                    # print "in if"
                    for oline in out_file:
                        query = oline.split(',')
                        for iline in inf:
                            # print iline
                            sentence = iline.split(',')
                            score = tc.get_jaccard(query[3], sentence[3])
                            data.append((sentence[0], sentence[2], score, query[3], sentence[3], sentence))
                        # print "data is :"+str(data)
                    out_file.close()
                    first_time_flag = 0
                else:
                    first_time_push(in_path, out_path, i)
                    first_time_flag = 1
                    print first_time_flag

        except:
            pass
        # print "seperate_relevent_tweet Error :"+str(i)
        print "first time flag for : " + str(i) + str(first_time_flag)
        temp_min = 1

        if first_time_flag == 0:
            ff = open('bm25/jac/' + str(i) + '_jaccard.txt', 'w')
            print "printing data " + str(data)
            # calculate minimum jaccard
            for d in data:
                if (d[2] < jaccard_thresold and d[2] < temp_min):
                    # push_tweet(d[0])
                    temp_min = d[2]
                    tweet_id = d[0]
                    queery_sentence = d[5]
                else:
                    pass
                ff.write(str(d) + ' \n')
            ff.close()

            if temp_min != 1:
                qid = get_query_id(i)
                # 				tweet_id = get_tweet_id(tweet_id)
                # ---------------------------------------------------------Change client id
                client_id = "4564546"
                lets_push(qid, tweet_id, client_id, i)

                with open('bm25/query/' + str(i) + '_pushed.txt', 'a') as fpush:
                    fpush.write(''.join(queery_sentence) + ' \nx`')

        i += 1


if __name__ == '__main__':
    calculate_jaccard(0.3, 203)


def first_time_push(inf, outf, i):
    # print "we are in first_time_push"
    with open(inf, 'r') as inf:
        first_line = inf.readline()
        with open(outf, 'w') as outf:
            outf.write(first_line)
        qid = get_query_id(i)
        tweet_id = get_tweet_id(first_line)
        # ---------------------------------------------------------Change client id
        client_id = "4564546"
        lets_push(qid, tweet_id, client_id, i)


def delete_file(query_size):
    i = 1
    while i < query_size:
        try:
            strin = 'bm25/query/' + str(i) + '.txt'
            os.remove(strin)
            strin = 'bm25/query/' + str(i) + '_relevent.txt'
            os.remove(strin)
            strin = 'bm25/query/' + str(i) + '_relevent_sorted.txt'
            os.remove(strin)

        except:
            pass
        i += 1


def evaluate_for_thresold(val_thresold, query_size):
    seperate_relevent_tweet(val_thresold, query_size)
    sort_file_result(query_size)
    save_files(query_size)
    calculate_jaccard(0.3, 200)
    delete_file(query_size)

    print "processed _relevent documents"
    #	if __name__ == '__main__':
    # sort_file_result(206)
    # evaluate_for_thresold(5.0,230)
