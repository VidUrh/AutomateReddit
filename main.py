import parameters
from GetRedditPosts import getPost
from GetTTS import getTTS
from CreateVideo import getImageClip,createVideo,getAudioFile,getVideoClip,getTextClip,getBackgroundClip
from getScreenshotDownload import getElementScreenshot,closeWindow
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
titleTTS = getTTS(titleString,0)
audioClip = getAudioFile('0')
audioItems = [audioClip]
imageItems = [getImageClip('0').set_duration(audioClip.duration)]
currentTime+=audioClip.duration

splitted = re.findall('.*?[.!\?]', textString)
i=0
while i<len(splitted):
    if len(splitted[i])<3:
        splitted[i-1]+=splitted[i]
        splitted.pop(i)
    else:
        i+=1


stripped = [x.strip() for x in splitted]
print(*stripped,sep='\n')
for fileSave,text in enumerate(stripped):
    getTTS(text, fileSave+1)
    
    audioClip = getAudioFile(fileSave+1)
    audioClip = audioClip.set_start(currentTime)
    num_words = 14

    textClip = getTextClip(text).set_duration(audioClip.duration)
    textClip = textClip.set_start(currentTime)
    imageItems.append(textClip)
    
    currentTime+=audioClip.duration
    
    audioItems.append(audioClip)

backgroundItems = [getBackgroundClip(currentTime)]
backgroundAudio = getAudioFile('BackgroundMusic').volumex(0.1)
backgroundAudio = backgroundAudio.set_duration(currentTime)
audioItems.append(backgroundAudio)

closeWindow()
createVideo(imageItems, audioItems, backgroundItems)











"""
getBackground(parameters.PEXELS_API_QUERY)
for item in askRedditPost:
    try: 
        success = getTTS(askRedditPost[item][0] + '\n' + askRedditPost[item][1],str(item)+parameters.TTS_API_CODEC)
        print('gotTTs')
        if not success:
            print("Problem TTS with " + str(item))
            raise Exception("TTSError")
        getElementScreenshot(askRedditPost[item][0],str(item))

        
        audioClipFile = getAudioFile(str(item)+parameters.TTS_API_CODEC)
        imageClipFile = getImageClip(str(item))
        videoClipFile = getVideoClip(str(item))


        audioClipFile = audioClipFile.set_start(currentTime)

        imageClipFile = imageClipFile.set_start(currentTime)
        imageClipFile = imageClipFile.set_duration(audioClipFile.duration)

        videoClipFile = videoClipFile.set_start(currentTimeBg)

        imageItems.append(imageClipFile)
        audioItems.append(audioClipFile)
        backgroundItems.append(videoClipFile)
        currentTime += audioClipFile.duration
        currentTimeBg += videoClipFile.duration
        print('gotItem: '+str(item))
        i+=1

    except Exception as e:
        print(e)
    if i>4:
        break
    
closeWindow()
video = createVideo(imageItems,audioItems,backgroundItems)
"""