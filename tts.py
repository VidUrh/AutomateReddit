"""This module is responsible for translating text to speech using the google text to speech api or the voicerss api.
    It will load the json file containing the posts from the reddit.py module.
    It will iterate through the posts and translate them to speech.
    It will save the audio files to the audio folder.
"""

############################################################################################################
#  Imports                                                                                                 #
############################################################################################################
import json
import configparser
import logging
import re
import requests
import os


############################################################################################################
#   Logging                                                                                                #
############################################################################################################
logger = logging.getLogger(__name__)

############################################################################################################
#   Requesting the text to speech api                                                                      #
############################################################################################################


def getSingleChunk(text, config):
    """ Function for requesting the text to speech api for a single chunk of text.

    Args:
        text (str): The text to be translated to speech.
        config (configparser): The configparser object.

    Returns:
        bool: True if the request was successful, False otherwise.
        requests.models.Response: The response from the text to speech api.
    """
    dataJSON = {
        "key": config["TTS"]["TTS_API_KEY"],
        "hl": config["TTS"]["TTS_API_LANGUAGE"],
        "v": config["TTS"]["TTS_API_VOICE"],
        "r": config["TTS"]["TTS_API_RATE"],
        "c": config["TTS"]["TTS_API_CODEC"],
        "f": config["TTS"]["TTS_API_FORMAT"],
        "src": text
    }
    response = requests.request(
        "POST", url=config["TTS"]["TTS_API_URL"], data=dataJSON)
    if True or response.status_code == 200:
        return True, response
    else:
        return False, response


def getTTS(text: list, postID: str, config: configparser):
    """ Function for requesting the text to speech api.

        Args:
            text (list): The text to be translated to speech (list from the json file).
            postID (str): The id of the post. Used for naming the audio folder.
            config (configparser): The configparser object.

        Returns:
            bool: True if the request was successful, False otherwise.
    """
    for chunkIndex, chunk in enumerate(text):
        ret_code, response = getSingleChunk(chunk, config)
        if ret_code:
            saveAudio(response, postID, chunkIndex, config)
        else:
            logger.critical(
                f"Error while requesting the text to speech api: {response.status_code} {response.reason}")
            break


def saveAudio(response, postID, chunkIndex, config):
    """This function will save the audio file to the audio folder.

    Args:
        response (requests.models.Response): The response from the text to speech api.
        chunkIndex (int): The index of the chunk. Used for naming the audio file.
        config (configparser): The configparser object.
    """
    # Create the folder for the audio files
    if not os.path.exists(f"{config['TTS']['TTS_AUDIO_FOLDER']}/{postID}"):
        os.makedirs(f"{config['TTS']['TTS_AUDIO_FOLDER']}/{postID}")

    with open(file=f"{config['TTS']['TTS_AUDIO_FOLDER']}/{postID}/{chunkIndex}.mp3", mode='wb') as f:
        f.write(response.content)
        f.close()
        logger.info(f"Saved audio file {chunkIndex}.mp3")


def splitTextToChunks(text, config) -> list:
    """This function will split the text into chunks by individual sentences.

    Args:
        text (str): The text to be split.
        config (configparser): The configparser object.

    Returns:
        list: A list containing the chunks of text.
    """
    return [text]
    splitted = re.findall('.*?[.!\?]', text)
    i = 0
    while i < len(splitted):
        if len(splitted[i]) < 3:
            splitted[i-1] += splitted[i]
            splitted.pop(i)
        else:
            i += 1

    stripped = [x.strip() for x in splitted]

    # Join the chunks of text to fit the max length of the api ()
    
    return stripped


def textToSpeech():
    """ Function for translating text to speech.
    """
    config = configparser.ConfigParser()
    config.read(filenames='config.ini')
    with open(file=config["REDDIT"]["POSTS_FILE"], mode='r') as f:
        posts = json.load(f)
        f.close()

    for post in posts:
        getTTS(posts[post], post, config)
        logger.info(f"Translated {post} to speech")


if __name__ == "__main__":
    textToSpeech()
