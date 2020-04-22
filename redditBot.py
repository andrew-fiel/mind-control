import praw
import datetime
from Utils.contentGeneration import CS370InANutshell


def makePostTitle(cl):
    return "Concentration Level: " + str(cl)


def makePostText(cl):
    time = datetime.datetime.now()
    nutshell = CS370InANutshell()
    bodyText = nutshell.getContent(cl)
    return bodyText + "\n\nThought up at " + str(time)


def selfPost(cl=0):
    reddit = praw.Reddit('bot1')
    sub = reddit.subreddit('u_quality-content-bot')
    sub.submit(title=makePostTitle(cl), selftext=makePostText(cl))


if __name__ == "__main__":
    selfPost(50)
