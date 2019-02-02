import tweepy
import time
import random
import json
import requests
import urllib


#twitterhandles = open('sorter.txt', 'r+', encoding="utf8")
#tweetfile = open('Tweets.txt', 'r+', encoding="utf8")
#fallow = open('Fallow.txt', 'r+', encoding="utf8")
#tweetslist = tweetfile.readlines()
fallowing = []
jokes = ["Q: What goes up and down but does not move? A: Stairs ", "Q: Where should a 500 pound alien go? A: On a diet  ", "Q: What did one toilet say to the other? A: You look a bit flushed. ", "Q: Why did the picture go to jail? A: Because it was framed. ", "Q: What did one wall say to the other wall? A: I'll meet you at the corner. ", "Q: What did the paper say to the pencil? A: Write on! ", "Q: What do you call a boy named Lee that no one talks to? A: Lonely ", "Q: What gets wetter the more it dries? A: A towel. ", "Q: Why do bicycles fall over? A: Because they are two-tired! ", "Q: Why do dragons sleep during the day? A: So they can fight knights! ", "Q: What did Cinderella say when her photos did not show up? A: Someday my prints will come! ", "Q: Why was the broom late?  A: It over swept! ", "Q: What part of the car is the laziest? A: The wheels, because they are always tired! ", "Q: What did the stamp say to the envelope?  A: Stick with me and we will go places! ", "Q: What is blue and goes ding dong? A: An Avon lady at the North Pole! ", "Q: We're you long in the hospital? A: No, I was the same size I am now! ", "Q: Why couldn't the pirate play cards?  A: Because he was sitting on the deck! ", "Q: What did the laundryman say to the impatient customer? A: Keep your shirt on! ", "Q: What's the difference between a TV and a newspaper? A: Ever tried swatting a fly with a TV? ", "Q: What did one elevator say to the other elevator? A: I think I'm coming down with something! ", "Q: Why was the belt arrested? A: Because it held up some pants! ", "Q: Why was everyone so tired on April 1st? A: They had just finished a March of 31 days.", "Q: Which hand is it better to write with? A: Neither, it's best to write with a pen! ", "Q: Why can't your nose be 12 inches long? A: Because then it would be a foot! ", "Q: What makes the calendar seem so popular? A: Because it has a lot of dates! ", "Q: Why did Mickey Mouse take a trip into space? A: He wanted to find Pluto! ", "Q: What is green and has yellow wheels? A: Grass…..I lied about the wheels! ", "Q: What is it that even the most careful person overlooks? A: Her nose! ", "Q: Did you hear about the robbery last night? A: Two clothes pins held up a pair of pants! ", "Q: Why do you go to bed every night? A: Because the bed won't come to you! ", "Q: Why did Billy go out with a prune? A: Because he couldn't find a date!  ", "Q: Why do eskimos do their laundry in Tide? A: Because it's too cold out-tide! ", "Q: How do you cure a headache? A: Put your head through a window and the pane will just disappear! ", "Q: What has four wheels and flies? A: A garbage truck! ", "Q: What kind of car does Mickey Mouse's wife drive? A: A minnie van! ", "Q: Why don't traffic lights ever go swimming? A: Because they take too long to change! ", "Q: Why did the man run around his bed? A: To catch up on his sleep! ", "Q: Why did the robber take a bath before he stole from the bank? A: He wanted to make a clean get away! "]
timepassed = 0

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

user = api.me()



def randomfromlist(List): #picks item from a list
    lenoflist = len(List)
    rand = random.randrange(0, lenoflist)
    return List[rand]



def friend(userid): #friends a specified user
    api.create_friendship(user_id = userid)



def waitnew(waittime): #waits in a way that displays debug info

    timepassed = 0

    while timepassed <= waittime:
        timepassed += 1
        time.sleep(1)
        print(waittime, timepassed)



def gettweets(userid): #Gets all tweets from a user useing userid
    tweetslist = []
    tweetsstatus = api.user_timeline(user_id = userid, tweet_mode = 'extended')

    for status in tweetsstatus:
        jsonstatus = json.dumps(status._json)
        dicstatus = json.loads(jsonstatus)
        Tweettxt = str(dicstatus['text'])
        tweetslist.append(Tweettxt)
    
    return tweetslist



def sendrandtwet(tweetslist):#dehh
    Senttweet = False
    while not Senttweet:
        try:
            endtweet = randomfromlist(tweetslist)
            print(endtweet)
            api.update_status(endtweet)
            Senttweet = True
        except tweepy.error.TweepError as e:
            print(e.reason)



def sendtweetwithimage(tweetdata, imagepath): #sends an image with a specified image path
    api.update_with_media(imagepath, status=tweetdata)

#recives user data
def getinfoforuser(userid='', userscreenname='', get_user_id=False, get_name=False, get_screen_name=False, get_discription=False, get_status_count=False, get_friends_count=False, get_fallowers_count=False):
    returnlist = []

    print("Getting data for " + userid)
    if userid != '':
        item = api.get_user(userid)
    elif userscreenname != '':
        item = api.get_user(screen_name = userscreenname)
    else:
        item = api.get_user(screen_name = 'okishia')

    if get_user_id == True:
        returnlist.append(item.id)
    if get_name == True:
        returnlist.append(item.name)
    if get_screen_name == True:
        returnlist.append(item.screen_name)
    if get_discription == True:
        returnlist.append(item.description)
    if get_status_count == True:
        returnlist.append(item.statuses_count)
    if get_friends_count == True:
        returnlist.append(item.friends_count)
    if get_fallowers_count == True:
        returnlist.append(item.followers_count)
    
    return returnlist



def getstatusfromtweetid(tweetid):
    status = api.get_status(tweetid)
    jsonstatus = json.dumps(status._json)
    dicstatus = json.loads(jsonstatus)
    Tweettxt = str(dicstatus['text'])
    return Tweettxt
    


def returnlasttweets(amountoftweets, includeretweets, screenname, returnid):
    stuff = api.user_timeline(screen_name = screenname, count = amountoftweets, include_rts=includeretweets, )
    returntweetlist = []
    for status in stuff:

        jsonstatus = json.dumps(status._json, ensure_ascii=False).encode('utf8')
        dictstatus = json.loads(jsonstatus)
        if returnid == True:
            print(dictstatus['id'])
            print(dictstatus['text'])
            returntweetlist.append([str(dictstatus['text']), dictstatus['id']])
        else:
            print(dictstatus['text'])
            returntweetlist.append(str(dictstatus['text']))
    return returntweetlist
    


def friendscreenname(screenname):
    return friend(getinfoforuser(userscreenname=screenname, get_user_id=True)[0])

def sendtweet(tweet): #Sends tweet you designate
    try:
        api.update_status(tweet)
    except:
        return tweepy.error.TweepError



#returnlasttweets(10, True, 'okishia', True)








#friends_userid = api.friends_ids() #gets all friends from okishia so it provides the data set
#tweetfile.truncate(0) 

"""for user_id in friends_userid:
    print(user_id)
    tweetlist2 = gettweets(user_id)
    print(tweetlist2)
    for tweet in tweetlist2:
        tweetfile.write(tweet)"""
"""
for tweet in tweetslist:
    tweet = emoji.demojize(tweet)
    tweet = tweet.replace('\n', '')
    tweetfile.write(tweet)
    tweetfile.write('\n')"""
