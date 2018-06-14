import os
import sys
from collections import Counter

def push(name,score,text):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "twitter_trend.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
    from tweet.models import Profile
    all = Profile.objects.all()
    #print "name ",name," score ",score," text ",text
    present = is_present(all,name,text)
    #print present
    if present:
        pass
    else:
        pr = Profile()
        pr.profile_name=name
        pr.save()
        all_new = Profile.objects.all()
        for each in all_new:
            each_str = str(each)
            if each_str == name:
                print "i am new"
                all_tweets = each.tweets_set.all()
                flag = jac_and_limit(all_tweets,text)
                if flag:
                    each.tweets_set.create(text = text)
                else:
                    print "issue with number or jacc"

def is_present(all,name,text):
    for each in all:
        each_str = str(each)
        if each_str == name:
            print 'i am old'
            all_tweets = each.tweets_set.all()
            flag = jac_and_limit(all_tweets, text)
            if flag:
                each.tweets_set.create(text=text)
            else:
                print "issue with number or jacc"

            # each.tweets_set.create(text = text)
            return True
    return False

def jac_and_limit(tweets,text):
    jac = 0.0
    tweet_count = 0
    for tweet in tweets:
        tweet = str(tweet)
        tweet_count += 1
        temp = get_jaccard(tweet,text)
        if temp > jac:
            jac = temp
    print tweet_count
    if jac < 0.4 and tweet_count < 10:
        return True
    else:
        return False


def get_jaccard(a,b):
    a=a.split()
    b=b.split()
    union = list(set(a+b))
    intersection = list(set(a) - (set(a)-set(b)))
#    print "Union - %s" % union
#    print "Intersection - %s" % intersection
    jaccard_coeff = float(len(intersection))/len(union)
#    print "Jaccard Coefficient is = %f " % jaccard_coeff
    return jaccard_coeff
