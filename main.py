import parameters
from GetRedditPosts import getPost
from GetTTS import getTTS
from CreateVideo import getImageClip,createVideo,getAudioFile,getVideoClip
from getScreenshotDownload import getElementScreenshot,closeWindow
from getVideoBackground import getBackground

askRedditPost = getPost(parameters.REDDIT_SUBREDDIT)


imageItems = []
audioItems = []
backgroundItems = []

currentTime = 0
currentTimeBg = 0

for x in askRedditPost:
    print(x,'\n',askRedditPost[x],'\n')

i=0
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