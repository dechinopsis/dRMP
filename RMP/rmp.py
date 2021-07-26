import datetime
import os
from time import sleep

import twitter
import tweepy


id = "119174866"
# 119174866 rmp
# 1188175357 ffnt
# 1353083279293952001 ffjk555

dt_consumer_key = "xxxxxxxxxxxxxxxxxxxxxxx"
dt_consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
dt_access_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
dt_access_secret = "xXxXxXxXxXxXxXxXxXxXxXxXxXxxXxXxXxXxXxXxXxXxX"
bot_access_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
bot_access_secret = "xXxXxXxXxXxXxXxXxXxXxXxXxXxxXxXxXxXxXxXxXxXxX"


class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if status.user.id_str != id:
            #print("\033[91mREJECTED", status)
            return

        sleep(20)
        try:
            apiB = twitter.Api(consumer_key=dt_consumer_key,
                               consumer_secret=dt_consumer_secret,
                               access_token_key=bot_access_key,
                               access_token_secret=bot_access_secret,
                               sleep_on_rate_limit=True)

            os.system('/Users/dtorres/PycharmProjects/screenshotPOC/venv/bin/python /Users/dtorres/PycharmProjects/screenshotPOC/main2.py '
                      + str(status.id))

            newStatus = \
                apiB.PostUpdate(media='/Users/dtorres/Documents/RMPSS/'+str(status.id)+'.png',
                                status=status.text.replace("@","_"))

            print(datetime.datetime.now(), "\033[92mREPLICATED SUCCESSFULLY ", status)

            try:
                if status.is_quote_status:
                    link = status.quoted_status_permalink.get('url')
                    apiB.PostUpdate(status=link, in_reply_to_status_id=newStatus.id)
            except Exception as exe:
                print(datetime.datetime.now(), "\033[91mERROR REPLYING MEDIA", exe, status)

        except Exception as exe:
            print(datetime.datetime.now(), "\033[91mERROR", exe, status)



    def on_error(self, status_code):
        print("\033[91mEncountered streaming error (", status_code, ")")


if __name__ == "__main__":
    auth = tweepy.OAuthHandler(dt_consumer_key, dt_consumer_secret)
    auth.set_access_token(dt_access_key, dt_access_secret)
    apiD = tweepy.API(auth)

    # initialize stream

    while True:
        sleep(3)
        try:
            print('\033[95mSTARTING',datetime.datetime.now())
            streamListener = StreamListener()
            stream = tweepy.Stream(auth=apiD.auth, listener=streamListener, tweet_mode='extended')
            sleep(3)
            stream.filter(follow=[id])
        except Exception as exe:
            print('\033[95mRESTARTING',datetime.datetime.now())
            print(datetime.datetime.now(), "\033[91mREASON", exe)