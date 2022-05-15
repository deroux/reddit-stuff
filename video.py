#!/usr/bin/python

import moviepy.editor as mpy
import gizeh as gz
from math import pi
import re
import sys
import librosa




VIDEO_SIZE = (640, 360)
BLUE = (59/255, 89/255, 152/255)
BLACK = (0/255, 0/255, 0/255)
GREEN = (176/255, 210/255, 63/255)
WHITE = (255, 255, 255)
WHITE_GIZEH = (1, 1, 1)
OUTPUT = "Let's build together"

def render_text(t):
    surface = gz.Surface(640, 360, bg_color=WHITE_GIZEH)
    arr = OUTPUT
    offset = 60
    for txt in arr:
        text = gz.text(
            txt, fontfamily="Robika",
            fontsize=20, fontweight='bold', fill=BLACK, xy=(320, offset))
        text.draw(surface)
        offset = offset + 20
    return surface.get_npimage()

def normalize_write_text(write_text):
    n = 50
    curr = n
    arr = []
    while (len(write_text) > n):
        if (write_text[curr] == ' '):
            arr.append(write_text[0:curr])
            print(write_text[0:curr])
            write_text = write_text[curr:]
            print(write_text)
            curr = n
        else:
            curr = curr + 1
    arr.append(write_text)
    print(arr)
    return arr

def create_video(write_text, duration, video_name, audio_file):
    global OUTPUT
    OUTPUT = normalize_write_text(write_text)
    text = mpy.VideoClip(render_text, duration=duration)
    video = mpy.CompositeVideoClip(
        [
            text.set_position(
                ('center', 'center'))
        ],
        size=VIDEO_SIZE).\
        on_color(
            color=WHITE,
            col_opacity=1).set_duration(duration)

    audioclip = mpy.AudioFileClip(audio_file).subclip(0, duration)
    videoclip = video.set_audio(audioclip)
    videoclip.write_videofile(video_name, codec='libx264', audio_codec='aac', fps=10, remove_temp=True)




if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("\nCall script like:", sys.argv[0], '<Text to render>', 'audio.mp3', 'output-filename.mp4')
        sys.exit(1)

    text = sys.argv[1]
    audio = sys.argv[2]
    filename = sys.argv[3]

    print(text)
    print(audio)
    print(filename)
    
    # TODO: escape characters like '
    # text = 'Now that PBS has announced they\'ll be televising the impeachment hearings, what will the drinking game rules be?'
    duration = librosa.get_duration(filename=audio)
    create_video(text, duration, filename, audio)
