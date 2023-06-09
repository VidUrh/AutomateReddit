"""
    This module contains all the functions in any way related to reddit.
    The module is responsible for downloading posts from reddit and saving them to a json file.
"""
############################################################################################################
#  Imports                                                                                                 #
############################################################################################################
import praw
import configparser
import json
import logging

############################################################################################################
#   Logging                                                                                                #
############################################################################################################

logger = logging.getLogger(__name__)


############################################################################################################
#   Filtering posts                                                                                        #
############################################################################################################
def isAcceptable(post):
    """ Function for checking if a post has been stickied or clicked on by me.

    Args:
        post (reddit post): The reddit post object from praw library.

    Returns:
        bool: True if the post is acceptable, False otherwise.
    """
    return not post.stickied and not post.clicked and not "trigger warning" in post.selftext.lower()


def isVisited(postID, config):
    """ Function for checking if a post has been visited before, 
        by checking the id of the post against the visited.txt file.

    Args:
        postID (str): The id of the post, gotten from the getID function.
        config (configparser): The configparser object.        

    Returns:
        bool: True if the post has been visited, False otherwise.
    """
    with open(file=config["REDDIT"]["VISITED"], mode='r') as f:
        visited = set(x.strip('\n') for x in f.readlines())
        return postID in visited

############################################################################################################
#   Functions                                                                                              #
############################################################################################################
def getID(post):
    """ Function for getting the id of a post.

    Args:
        post (reddit post): The reddit post object from praw library.

    Returns:
        str: The id of the post.
    """
    return post.id_from_url(post.url)

############################################################################################################
#   Main                                                                                                   #
############################################################################################################
def getPosts():
    """
    This function will get the top posts from a subreddit and save them to a json file.    
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    subreddit = praw.Reddit(client_id=config['REDDIT']['API_KEY'],
                            client_secret=config['REDDIT']['API_SECRET'],
                            user_agent=config['REDDIT']['USER_AGENT'],
                            username=config['REDDIT']['USERNAME']
                            ).subreddit(config['REDDIT']['SUBREDDIT'])

    # Get the top posts from the subreddit.
    hottest_posts = subreddit.hot(limit=int(config['REDDIT']['POST_LIMIT']))

    # Variable for storing the posts, later dumped to json file.
    posts = dict()

    for post in hottest_posts:

        postID = getID(post)  # Get the id of the post.
        logger.info(f"Checking post: {postID}")
        if isAcceptable(post) and not isVisited(postID, config):
            # Add the post to the posts dictionary.
            posts[postID] = [post.title, post.selftext]

            # Add the post id to the visited.txt file.
            with open(file=config["REDDIT"]["VISITED"], mode='a') as f:
                f.write(f"{postID}\n")
                
            logger.info(f"Added post: {postID}")
    # Dump the posts to a json file.
    with open(file=config["REDDIT"]["POSTS_FILE"], mode='w') as postsFile:
        json.dump(posts, postsFile, indent=6)
        postsFile.close()
        logger.info(f"Saved posts to file: {config['REDDIT']['POSTS_FILE']}")
    logger.info("Finished getting posts from reddit.")
