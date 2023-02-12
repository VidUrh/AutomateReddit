import parameters
import moviepy.editor as mpy
from datetime import datetime
from random import randrange


def getAudioFile(name):
    return mpy.AudioFileClip(parameters.SOUNDS_FOLDER+str(name)+parameters.TTS_API_CODEC)


def getImageClip(title):
    image = mpy.ImageClip(parameters.IMAGES_FOLDER +
                          title + parameters.IMAGES_CODEC)
    image = image.set_position('center')
    image = image.resize(width=parameters.MOVIEPY_WIDTH -
                         parameters.MOVIEPY_BORDERSIZEOUTER)
    return image


def getVideoClip(title):
    return mpy.VideoFileClip(parameters.MOVIEPY_BACKGROUNDFILE + title + parameters.MOVIEPY_VIDEOCODEC).resize(width=parameters.MOVIEPY_WIDTH)


def getTextClip(text):
    textClip = mpy.TextClip(text,
                            fontsize=30,
                            font='Noto-Sans',
                            size=(parameters.MOVIEPY_WIDTH -
                                  parameters.MOVIEPY_BORDERSIZE, 0),
                            color='black',
                            bg_color='white',
                            method='caption'
                            ).set_position('center')
    return textClip


def getBackgroundClip(time):
    bg = mpy.VideoFileClip(parameters.VIDEOS_FOLDER +
                           "Background/minecraftBackground.mp4")
    randomnum = randrange(0, int(bg.duration-time), 1)
    bg = bg.subclip(randomnum, randomnum+time)
    bg = bg.crop(width=720, height=1280)
    return bg


def createVideo(imageItems, audioItems, backgroundItems):
    background = mpy.CompositeVideoClip(backgroundItems)
    audioClip = mpy.CompositeAudioClip(audioItems)
    # background = background.loop(duration = audioClip.duration)
    imageItems = [background] + imageItems

    final_clip = mpy.CompositeVideoClip(imageItems)
    final_clip.audio = audioClip

    # save file
    final_clip.write_videofile(parameters.MOVIEPY_OUTPUTFILE + datetime.now().strftime("%B_%d_%H-%M") + parameters.MOVIEPY_VIDEOCODEC, threads=4, fps=24,
                               codec=parameters.MOVIEPY_VCODEC,
                               preset=parameters.MOVIEPY_COMPRESSION,
                               ffmpeg_params=["-crf", parameters.MOVIEPY_QUALITY])

    background.close()
    audioClip.close()


if __name__ == "__main__":
    print(*mpy.TextClip.list('font'), sep='\n')
