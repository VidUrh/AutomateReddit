import requests
import parameters
import json
import urllib.request

 
def getBackground(query):

    url = parameters.PEXELS_API_ENDPOINT  #"https://pexelsdimasv1.p.rapidapi.com/v1/search"

    querystring = {"query":query,"locale":"en-US","size":parameters.PEXELS_API_SIZE,"orientation":parameters.PEXELS_API_ORIENTATION}

    headers = {
        "Authorization": parameters.PEXELS_API_KEY
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    jsonFile = json.loads(response.content)
    videos = jsonFile['videos']
    i=0
    count = 0
    while i < len(videos):
        video = videos[i]
        
        possibleVideo = list(filter(lambda x: x['quality']=='sd', video['video_files']))
        if len(possibleVideo):
            possibleVideo = sorted(possibleVideo,key = lambda x : x['width'])[-1]
            print('Downloading video background item:',count)
            urllib.request.urlretrieve(possibleVideo['link'], parameters.MOVIEPY_BACKGROUNDFILE+str(count)+'.mp4')
            count+=1
        if count > 4:
            break
        i+=1
    return count
         
if __name__ == "__main__":
    status = getBackground('parkour1')
    print(status)