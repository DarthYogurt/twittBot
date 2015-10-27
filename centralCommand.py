
#!/usr/bin/env python
""" Main HQ that checks times then sends out twitter bot agents
1) Crawler Bot
2) Follow Bot
3) Followed By Bot
4) Unfollow Bot
5) Scheduler Agent


Daily Crawler bot finds new people to follow
Scheduler decides when to execute the follow, hourly
Follow bot executed hourly and follows those who are scheduled

Followed By bot, checks to see if you're unfollowed, or not followed
Scheduler decides when to unfollow
Unfollow Bot will activate at a time from scheduler
"""

import datetime
import oauth2
import json

import config

TAGS = [
    "#gamer"
]

def main_cortex():
    #Get time
    current_time = datetime.datetime.utcnow()
    current_hour = current_time.hour

    # if current_hour == 0:
    if current_hour:
        crawler_bot(TAGS)

def crowler_bot(tags):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=%23gamer'
    response = json.loads(oauth_req( url, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET, "GET" ))
    tweets = response['statuses']
    True

    # follow(tweets[0]['user']['id_str'])


def list_manager_bot():
    url = 'https://api.twitter.com/1.1/friends/list.json'
    user_list = json.loads(oauth_req(url, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET, "GET"))

    for i in range(len(user_list)):
        print i
        # if user_list[i]['follow_request_sent'] == True:
            # print user_list[i]['name'], user_list[i]['follow_request_sent']

def follow(id):

    url = 'https://api.twitter.com/1.1/friendships/create.json?user_id='+ id +'&follow=true'
    response = json.loads(oauth_req( url, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET, "POST" ))
    print response




def oauth_req(url, key, secret, http_method, post_body='', http_headers=None):
    consumer = oauth2.Consumer(key=config.CONSUMER_KEY, secret=config.CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content



# main_cortex()
# id_crawler(TAGS)

list_manager_bot()




