import parameters
import moviepy.editor as mpy
from datetime import datetime

def getAudioFile(name):
    return mpy.AudioFileClip(parameters.SOUNDS_FOLDER+name)


def getImageClip(title):
    image = mpy.ImageClip(parameters.IMAGES_FOLDER + title + parameters.IMAGES_CODEC)
    image = image.set_position(('center',0.4),relative=True)
    image = image.resize(width=parameters.MOVIEPY_WIDTH-50)
    return image


def createVideo(imageItems, audioItems):
    # load 
    background = mpy.VideoFileClip(parameters.MOVIEPY_BACKGROUNDFILE).resize(width=parameters.MOVIEPY_WIDTH)
    audioClip = mpy.CompositeAudioClip(audioItems)    
    background = background.loop(duration = audioClip.duration)
    imageItems = [background] + imageItems

    final_clip = mpy.CompositeVideoClip(imageItems)
    final_clip.audio = audioClip

    # save file
    final_clip.write_videofile(parameters.MOVIEPY_OUTPUTFILE + datetime.now().strftime("%B_%d_%H-%M") + parameters.MOVIEPY_VIDEOCODEC, threads=4, fps=24,
                               codec=parameters.MOVIEPY_VCODEC,
                               preset=parameters.MOVIEPY_COMPRESSION,
                               ffmpeg_params=["-crf",parameters.MOVIEPY_QUALITY])

    background.close()
    audioClip.close()


