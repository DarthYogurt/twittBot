
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


TAGS = [
    "gamer"
]

def main_cortex():
    #Get time
    current_time = datetime.datetime.utcnow()
    current_hour = current_time.hour


    # if current_hour == 0:
    if current_hour:
        id_crawler(TAGS)


def id_crawler(tags):
    True





main_cortex()


