__author__ = 'Nick Hirakawa'

from parse import *
from query import QueryProcessor
import operator
import bm25_result_parser as rparser
import ss_push as push

# def main():

def start_bm25():
    # print "i was HERE!!!"
    thresh = open('/home/deep/TwitterTrend/text/Threshold.txt')
    th = []
    for each in thresh:
        th.append(each.strip())

    prof = open('/home/deep/TwitterTrend/text/ProfileName.txt')
    pro = []
    for each in prof:
        pro.append(each.strip())

    qp = QueryParser(filename='text/query.txt')
    cp = CorpusParser(filename='corpus111.txt')
    qp.parse()
    queries = qp.get_queries()
    #print "Q is ",queries
    cp.parse()
    corpus = cp.get_corpus()
    #print "c is ", corpus
    proc = QueryProcessor(queries, corpus)
    results = proc.run()
    print results
    qid = 1
    bm25_output_list = []
    for result in results:
        threshold = th[qid-1]
        profile_name = pro[qid-1]
        print threshold
        print profile_name
        sorted_x = sorted(result.iteritems(), key=operator.itemgetter(1))
        sorted_x.reverse()
        index = 0
        for i in sorted_x[:100]:
            tweet_text = cp.get_text(i[0])
            tmp = (qid, i[0], index, i[1])
            # print str(tmp)
            #print "yaay"
            text = '{:>1}, {:>4}, {:>2}, {:>12}'.format(*tmp) + ", " + tweet_text
            flag = threshold_check(i[1],threshold)
            if flag:
                push.push(profile_name,i[1],tweet_text)
                bm25_output_list.append(text)
            index += 1
        qid += 1

    with open('ss_b'
              'm25_output.txt', 'a') as f:
        for item in bm25_output_list:
            f.write(item + ' \n')
    rparser.seperate_store_result()


def threshold_check(score, threshold):
    if score >= int(threshold):
        return True
    else:
        return False

if __name__ == '__main__':
    start_bm25()
