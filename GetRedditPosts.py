import praw
import parameters

reddit = praw.Reddit(client_id=parameters.REDDIT_API_KEY,
                     client_secret=parameters.REDDIT_API_SECRET,
                     user_agent='test_bot', 
                     username='Downtown_Ad_1647'
                    )
f = open("visited.txt", "a")

with open("visited.txt", "r") as w:
    visited = set() #set(x.strip('\n') for x in w.readlines())

def getPost(subredditTopic):
    post={}
    subreddit = reddit.subreddit(subredditTopic)
    hot_python = subreddit.hot(limit=3)
    index = 0
    for submission in hot_python:
        sub_id = submission.id_from_url(submission.url)
        if not submission.stickied and not submission.clicked and sub_id not in visited:
            post[index] = [submission.title,submission.selftext]
            index+=1
            f.write(sub_id+'\n')
            break
    f.close()
    return post

if __name__ == '__main__':

    post = getPost(parameters.REDDIT_SUBREDDIT)
    [print(post[x]) for x in post]