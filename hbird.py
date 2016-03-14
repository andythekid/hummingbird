#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = ""
consumer_secret = ""
# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_key = ""
access_secret = ""

import tweepy, sys, getopt
from datetime import datetime

def usage(exitCode):
    print "Usage: %s [options]" % sys.argv[0]
    print """
Options:
    -h, --help                   show this help message and exit
    -d DATE, --date=DATE         set the date of deleted tweets, ex.: 30.06.1934
    -t HASHTAG, --tag=HASHTAG    set the hashtag of deleted tweets, ex.: NiceShirts
    -c NUMBER, --counter=NUMBER  set the number of deleted tweets
    """
    sys.exit(exitCode)
    # usage()

def init():
    # Аунтификация
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)
    # init()

def main():
    date = None
    tag = None
    count = 1
    # Проверяем аргументы командной строки
    if 1 == len(sys.argv):
        usage(2)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:d:c:", ["help", "tag=", "date=", "count="])
        for o, a in opts:
            if o in ("-t", "--tag"):
                tag = "#" + str(a) +" "
                tag = unicode(tag, "utf-8")
            elif o in ("-d", "--date"):
                date = datetime.strptime(a, "%d.%m.%Y")
            elif o in ("-c", "--counter"):
                count = int(a)
            elif o in ("-h", "--help"):
                usage(0)
            else:
                assert False, "unknown option"
    except Exception as err:
        print "Error: " + str(err)
        usage(2)
    api = init()
    delCount = 0
    # Переменные визуализации процесса
    if count < 10:
        step = 1
    else:
        step = count/10 # шаг (10%)
    c = 0           # счетчик запросов
    sys.stdout = sys.stderr # небуферизованный вывод
    # Если выставлены и хэштег и дата (или наоборот) - выходим
    if ((None == tag) and (None == date)) or ((None != tag) and (None != date)):
        print "Sorry, must set date OR tag."
        usage(2)
    # Удаление по дате
    elif None != date:
        print "[",
        for status in tweepy.Cursor(api.user_timeline, user_id=api.me).items(count):
            c += 1
            if 0 == (c % step):
                print '=',
            if status.created_at.date() == date.date():
                api.destroy_status(status.id)
                delCount += 1
    # Удаление по хэштегу
    elif None != tag:
        print "[",
        for status in tweepy.Cursor(api.user_timeline, user_id=api.me).items(count):
            c += 1
            if 0 == (c % step):
                print '=',
            if -1 != status.text.find(tag):
                api.destroy_status(status.id)
                delCount += 1
    print "]"
    print "%d tweets deleted." % delCount
    # main()

if __name__ == '__main__':
    main()
