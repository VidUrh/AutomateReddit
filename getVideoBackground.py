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
    for i,video in enumerate(videos[:6]):
        print(video['video_files'][0]['link'])
        urllib.request.urlretrieve(video['video_files'][-2]['link'], parameters.MOVIEPY_BACKGROUNDFILE+str(i)+'.mp4')
        
if __name__ == "__main__":
    status = getBackground('parkour')
    print(status)