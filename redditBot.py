import praw
import datetime
from Utils.contentGeneration import CS370InANutshell
import os
import pytz


def makePostTitle(cl):
    return "Concentration Level: " + str(cl)


def makePostText(cl):
    startTime = getTime()
    nutshell = CS370InANutshell()
    bodyText = nutshell.getContent(cl)
    endTime = getTime()
    timeDif = endTime - startTime

    # return content of future reddit post
    return (bodyText +
            "\n\nThought up on " + endTime.strftime("%A, %B %d, %Y @ %I:%M:%S:%f %p %Z") +
            "\n\nTook " + str(timeDif.seconds) + "." + str(timeDif.microseconds) + " seconds to generate.")


def getTime():
    # get current time in utc
    time = datetime.datetime.utcnow()
    mdt = pytz.timezone("America/Denver")
    # convert timezone to Denver/mdt time
    return pytz.utc.localize(time, is_dst=None).astimezone(mdt)


def selfPost(cl=0):
    # checks for heroku env variable that indicates deployed
    if os.environ.get('DEPLOYED', 'false') != 'false':
        reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                             client_secret=os.environ['CLIENT_SECRET'],
                             password=os.environ['PASSWORD'],
                             username=os.environ['USERNAME'],
                             user_agent=os.environ['USER_AGENT'])
    else:
        # praw.ini file works locally, but would expose keys if pushed
        reddit = praw.Reddit('bot1')
    sub = reddit.subreddit('u_quality-content-bot')
    sub.submit(title=makePostTitle(cl), selftext=makePostText(cl))


if __name__ == "__main__":
    selfPost(50)
