"""
    This script will automate the process of creating a youtube reddit reading video and publishing it to youtube.
    It will get the top 5 posts from a subreddit using the praw library.
    It will translate the text to speech using the google text to speech api or the voicerss api.
    It will create reddit screenshots using the selenium library.
    It will create a video using the moviepy library.
    It will upload the video to youtube using the google api.
"""
############################################################################################################
#  Imports                                                                                                 #
############################################################################################################
import logging
from reddit import getPosts
#from tts import textToSpeech
# from screenshot import createScreenshots
# from video import createVideo
# from youtube import uploadVideo

############################################################################################################
#   Logging                                                                                                #
############################################################################################################
logging.basicConfig(level=logging.INFO)

############################################################################################################
#   Downloading the top posts                                                                              #
############################################################################################################
if __name__ == "__main__":
    getPosts()
    #textToSpeech()
