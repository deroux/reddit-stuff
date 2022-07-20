
# Import the required module for text
# to speech conversion
import os
import subprocess
import sys

import numpy as np
from gtts import gTTS
from numpy.random import uniform
from pydub import AudioSegment

n = len(sys.argv)

if (n != 3):
    print("\nCall script like:", sys.argv[0], '<Text>', 'outfile.mp3')
    sys.exit(1)

# necessary for TTS conversion


def execute_unix(inputcommand):
    p = subprocess.Popen(inputcommand, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    return output


text = sys.argv[1]
filename = sys.argv[2]
# The text that you want to convert to audio
mytext = text

# Language in which you want to convert
language = 'en'

# gTTS implementation
# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
# myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
# myobj.save(filename)  # test.mp3

# modify pitch as speed of video will be increased
# sound = AudioSegment.from_file(filename, format=filename[-3:])
# octaves = -1

# new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
# hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
# hipitch_sound = hipitch_sound.set_frame_rate(44100)
# export / save pitch changed sound
# hipitch_sound.export(filename, format="mp3")

# TTS implementation https://github.com/mozilla/TTS
cmd="tts --text \"{text}\" --out_path {file}".format(text = mytext, file = filename)
os.system(cmd)
