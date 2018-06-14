import json
import evaluator
import bm25.bm25_result_parser as rparser
count = 0
i = 0
for hour in range(0,24):
    jfile = open("/home/shyamal/PycharmProjects/TwitterTrend/29/ {0}.txt".format(hour), 'r')


    def bulk_tweet(i):
        evaluator.set_data(i)
    skip = 0
    tweets_list = []
    for line in jfile:
        if skip % 2 == 0:
            line = line.strip()
            count += 1
            #    tweets_list.append(json.dumps(data))
            tweets_list.append(line)
            # print "i is ",i
            if count % 100 == 0:
                print "%d statuses processed" % count
                #        print tweets_list

                i = i % 10
                with open(str(i) + '_temp_tweet.txt', 'w') as f:
                    f.write(json.dumps(tweets_list))
                    tweets_list = []
                    # print tweets_list,"it is empty"
                bulk_tweet(i)
                i += 1
                # print i
                # bulk_tweet()
        skip += 1

            # it will call evaluate_for_thresold function after defined count.
        # if count % 40000 == 0:
        #     rparser.evaluate_for_thresold(8, 205)



