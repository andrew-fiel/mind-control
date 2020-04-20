import praw
import datetime


def makePostTitle(cl):
    return "Concentration Level: " + str(cl)


def makePostText():
    time = datetime.datetime.now()
    bodyText = "dummy body text"
    return bodyText + "\n\nRecieved at " + str(time)


def selfPost(cl=0):
    reddit = praw.Reddit('bot1')
    sub = reddit.subreddit('u_quality-content-bot')
    sub.submit(title=makePostTitle(cl), selftext=makePostText())


if __name__ == "__main__":
    selfPost(10)
