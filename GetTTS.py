import requests
import parameters


def getTTS(text,fileSave):
    dataJSON = {
        "key": parameters.TTS_API_KEY,
        "hl": parameters.TTS_API_LANGUAGE,
        "v": parameters.TTS_API_VOICE,
        "r": parameters.TTS_API_RATE,
        "c": parameters.TTS_API_CODEC,
        "f": parameters.TTS_API_FORMAT,
        "src":text
    }

    response = requests.request("POST", parameters.TTS_API_URL, params=dataJSON)
    if response.status_code==200:
        with open(parameters.SOUNDS_FOLDER+str(fileSave)+parameters.TTS_API_CODEC, 'wb') as f:
            f.write(response.content)
        f.close()
        return True
    else:
        return False
        
if __name__ == "__main__":
    status = getTTS('I like big butts and i cannot lie!')
    print(status)