import parameters
from GetRedditPosts import getPost
from GetTTS import getTTS
from CreateVideo import getImageClip,createVideo,getAudioFile
from getScreenshotDownload import getElementScreenshot,closeWindow

askRedditPost = getPost(parameters.REDDIT_SUBREDDIT)


imageItems = []
audioItems = []
currentTime = 0

print(askRedditPost)
i=0

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
        audioClipFile = audioClipFile.set_start(currentTime)

        imageClipFile = imageClipFile.set_start(currentTime)
        imageClipFile = imageClipFile.set_duration(audioClipFile.duration)
        imageItems.append(imageClipFile)
        audioItems.append(audioClipFile)
        currentTime += audioClipFile.duration
        print('gotItem'+str(item))
        i+=1

    except Exception as e:
        print(e)
    if i>4:
        break
    
closeWindow()
video = createVideo(imageItems,audioItems)