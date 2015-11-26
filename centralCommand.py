
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

PROBLEM - after list reaches greater than 36000, then will not be able to compare lists. Will need modification
"""

import datetime
import oauth2
import json
import random

import config
import dbCommand

#Test vars# FOLLOW_ME = [29307927, 128046970, 3168160135, 2990661978, 961343107, 3096940393, 3233346379, 1514161634, 2893791550, 111772198, 20454008, 2440137514, 3138048128, 40389230, 42070873, 2604579602, 3031604363, 122100715, 1414116312, 241425722, 2456008706, 2439058668, 2854195674, 2476509679, 2373234356, 980244326, 623481824, 2853981112, 2744636001, 131021790, 2603893298, 2336398303, 267390486, 537471180, 2471741688, 2413297212, 2836398421, 2822924582, 1465185794, 2458801806, 1263030198, 2685289070, 2257045110, 367268428, 25787449, 2350581756, 2595516823, 2238052714, 2790435293, 161871121, 715042730, 2185889666, 2492012544, 2883293332, 2881315559, 2539029462, 2850270525, 2725307480, 2879613747, 2577504081, 2781822957, 2805604317, 469960963, 317630994, 549023176, 2486054191, 567029347, 756562831, 2827182458, 2717203222, 2185087887, 2869748964, 2869997285, 1497143617, 2823896811, 2832237452, 1160804330, 2836310852, 1921199455, 1200024332, 386408124, 1198278313, 2732586197, 234765685, 2470908158, 159364516, 6173842, 1656468925, 16217345, 2843597890, 16887175, 554102447, 1965608106, 20619143, 2679690074, 1145180510, 1923729505, 368666488, 1137609062, 2419451328, 157788452, 5606352, 1377326713, 2861381792, 2515634902, 2768116336, 493923757, 318594215, 29590940, 41103446, 1452657685, 2180120179, 40246348, 2586765685, 2829290401, 709226545, 315814665, 15276573, 15880163, 2861129666, 16819961, 2647258484, 2185296877, 2326094407, 344836457, 2199502159, 28501665, 19312115, 20953171, 47332078, 178566085, 608668915, 168205825, 242222569, 25506205, 11890702, 33191389, 7244502, 2698485211, 2556965180, 764614892, 2260693675, 598244406, 47489753, 493671024, 2829932528, 137473586, 335536844, 1957221386, 203983655, 2188711458, 1598571691, 2438765444, 336243889, 221020763, 2227306776, 2612898218, 2363361806, 2421545378, 320808486, 2370185519, 2780047920, 2162921304, 2177126275, 20747741, 21158690, 90964854, 1383883662, 2578937982, 2815530956, 273034026, 2593297898, 161469460, 725983519, 2802603349, 2614144598, 2773149725, 1665476762, 2645807281, 876053802, 2785154322, 448788827, 2621023270, 1656749239, 2180255822, 1669007538, 225035160, 2468473939, 2812782110, 948444535, 1260639133, 310280920, 19782698, 2651584152, 40188143, 2812385954, 1486379629, 2343006698, 245396123, 770376163, 2303783317, 19604744, 716901834, 2502055213, 629701472, 1571560136, 2815688646, 2232131719, 18776017, 2207520854, 16567106, 76774950, 22841103, 96548127, 721126415, 2235753684, 2414990580, 14223818, 2238044108, 2309061030, 176232098, 1920011466, 2713797863, 2519613291, 2747277700, 1956497142, 1479886982, 520922874, 13871852, 213184972, 226468273, 2171797766, 256445426, 1275135176, 330335226, 47709951, 17265257, 61537286, 49598100, 19607400, 32252881, 192641332, 740212208, 2260974454, 17610785, 417491069, 14417215, 1877210413, 48424601, 2384077874, 19879128, 2246704694, 105297123, 68257605, 2327565617, 2493905629, 1327446078, 878905860, 19413393, 22258315, 20273398, 6240732, 11928542, 21770389, 2409451298, 14716974, 556167733, 143928271, 309366491, 2333845129, 19631395, 972651, 60642052, 816653, 24742040, 7157132, 18927441, 14922225, 15234657, 61040833, 10671602, 61033129, 36803580, 8732992, 16736535, 1735723976, 15846407]
TAGS = [
    "gamer",
    "starwars"
]
BASE_URL = 'https://api.twitter.com/1.1/'

# def main_cortex():
#     #Get time
#     current_time = datetime.datetime.utcnow()
#     current_hour = current_time.hour
#
#     # if current_hour == 0:
#     # if current_hour:
#     #     crawler_bot(TAGS)
#
#     #run hourly
#     # list_manager_bot()

def crawler_bot(tags):
    url = BASE_URL + 'search/tweets.json?q=' + str(random.choice(tags))
    response = json.loads(oauth_req( url, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET, "GET" ))
    tweets = response['statuses']

    if 'errors' in response:
        print response['errors']

    usr = random.choice(tweets)
    dbCommand.add_id(usr['user']['id_str'], following=True, following_me=False)
    follow(usr['user']['id_str'])

def get_twitter_friend_list(list, cursor):
    '''
    Needs to paginate due to twitter rest api. Using recursive solution to get data.
    :param list:
    List of users
    :param cursor:
     0 = end of pagination
     1 = start of pagination
     24324141 = twitter next cursor info
    :return:

        '''
    if cursor > 1:
        url = BASE_URL + 'friends/ids.json?cursor=' + str(cursor)
    elif cursor == 0:
        return list
    elif cursor == 1:
        url = BASE_URL + 'friends/ids.json'
    response = json.loads(oauth_req(url, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET, "GET"))
    if 'errors' in response:
        print response['errors']
        return []
    id_list = response['ids']
    for i in range(len(id_list)):
        list.append(id_list[i])

    return get_twitter_friend_list(list, response['next_cursor'])

def get_twitter_follower_list(list, cursor):
    if cursor > 1:
        url = BASE_URL + 'followers/ids.json?count=5000&cursor=' + str(cursor)
    elif cursor == 0:
        return list
    elif cursor == 1:
        url = BASE_URL + 'followers/ids.json?count=5000'
    response = json.loads(oauth_req(url, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET, "GET"))
    id_list = response['ids']
    for i in range(len(id_list)):
        list.append(id_list[i])

    return get_twitter_follower_list(list, response['next_cursor'])

def update_friend_list_db():
    twitter_friend_list = get_twitter_friend_list([],1)
    for id in twitter_friend_list:
        user = dbCommand.get_user_by_id(id)
        if user == None:
             dbCommand.add_id(id, following=True, following_me=False)
             dbCommand.update_followed_time(id)
        else:
            if user['following'] == False:
                dbCommand.update_following(id, True)
                dbCommand.update_followed_time(id)

def update_following_me_db():
    twitter_follower_list = get_twitter_follower_list([],1)
    for id in twitter_follower_list:
        user = dbCommand.get_user_by_id(id)
        if user == None:
            dbCommand.add_id(id, following=False, following_me=True)
        else:
            dbCommand.update_following_me(id, following_me=True)

def list_manager_bot():
    '''
    Compare with list in DB. Sync
    if not in db then add

    :return:
    '''
    update_friend_list_db()  #people who i am following
    update_following_me_db()  #people who are following me

def remove_non_follower():
    users = dbCommand.get_users( following = True, following_me = False, days = 0)
    if len(users) < 1:
        return
    usr =  random.choice(users)
    un_follow( usr['id'] )
    dbCommand.update_following( usr['id'], False )
    dbCommand.update_unfollowed_time(usr['id'])

def add_follower_following_me():
    users = dbCommand.get_users( following = False, following_me = True, days = 0)
    if len(users) < 1:
        return
    usr =  random.choice(users)
    follow(usr['id'])
    dbCommand.update_following( usr['id'], True )
    dbCommand.update_followed_time( usr['id'] )
    # print usr

def retry_add_non_follower():
    users = dbCommand.get_users( following = False, following_me = False, days = 2)
    if len(users) < 1:
        return
    usr = random.choice(users)
    follow( usr['id'] )
    dbCommand.update_following( usr['id'], True )
    dbCommand.update_followed_time( usr['id'] )

def follow(id):
    url = BASE_URL + 'friendships/create.json?user_id='+ id +'&follow=true'
    json.loads(oauth_req( url, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET, "POST" ))
    dbCommand.update_following( id, True )
    print "followed",id

def un_follow(id):
    url = BASE_URL + 'friendships/destroy.json?user_id=' + id
    json.loads(oauth_req( url, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET, "POST" ))
    print "unfollowed",id

def oauth_req(url, key, secret, http_method, post_body='', http_headers=None):
    consumer = oauth2.Consumer(key=config.CONSUMER_KEY, secret=config.CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

def get_counts():

    following = dbCommand.get_twitter_follow_list().count()
    following_me = dbCommand.get_twitter_follow_me_list().count()
    return "Following", following, "Following_Me:", following_me

def rate_limit():
    url = BASE_URL + 'application/rate_limit_status.json'
    response = json.loads(oauth_req( url, config.ACCESS_TOKEN, config.ACCESS_TOKEN_SECRET, "GET" ))
    print '/friends/ids',response['resources']['friends']['/friends/ids']
    print '/followers/ids',response['resources']['followers']['/followers/ids']
# main_cortex()

print datetime.datetime.now()

# a = get_twitter_friend_list([],1)

list_manager_bot()
crawler_bot(TAGS)
crawler_bot(TAGS)
remove_non_follower()
remove_non_follower()
remove_non_follower()
remove_non_follower()
add_follower_following_me()
retry_add_non_follower()
print get_counts()
rate_limit()



