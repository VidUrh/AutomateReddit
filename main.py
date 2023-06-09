import parameters
from GetRedditPosts import getPost
from GetTTS import getTTS
from CreateVideo import getImageClip, createVideo, getAudioFile, getVideoClip, getTextClip, getBackgroundClip
from getScreenshotDownload import getElementScreenshot, closeWindow
from getVideoBackground import getBackground
import re


askRedditPost = getPost(parameters.REDDIT_SUBREDDIT)

imageItems = []
audioItems = []
backgroundItems = []

currentTime = 0
currentTimeBg = 0

titleString = askRedditPost[0][0]
textString = askRedditPost[0][1]
titleImage = getElementScreenshot(titleString, '0')
titleTTS = getTTS(titleString, 0)
audioClip = getAudioFile('0')
audioItems = [audioClip]
imageItems = [getImageClip('0').set_duration(audioClip.duration)]
currentTime += audioClip.duration

splitted = re.findall('.*?[.!\?]', textString)
i = 0
while i < len(splitted):
    if len(splitted[i]) < 3:
        splitted[i-1] += splitted[i]
        splitted.pop(i)
    else:
        i += 1


stripped = [x.strip() for x in splitted]
print(*stripped, sep='\n')
for fileSave, text in enumerate(stripped):
    getTTS(text, fileSave+1)

    audioClip = getAudioFile(fileSave+1)
    audioClip = audioClip.set_start(currentTime)
    num_words = 14

    textClip = getTextClip(text).set_duration(audioClip.duration)
    textClip = textClip.set_start(currentTime)
    imageItems.append(textClip)

    currentTime += audioClip.duration

    audioItems.append(audioClip)

backgroundItems = [getBackgroundClip(currentTime)]
backgroundAudio = getAudioFile('BackgroundMusic').volumex(0.1)
backgroundAudio = backgroundAudio.set_duration(currentTime)
audioItems.append(backgroundAudio)

closeWindow()
createVideo(imageItems, audioItems, backgroundItems)
