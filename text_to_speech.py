
# Import the required module for text 
# to speech conversion
from gtts import gTTS
import os, sys
from pydub import AudioSegment
from numpy.random import uniform
import numpy as np
  
n = len(sys.argv)

if (n != 3):
    print("\nCall script like:", sys.argv[0], '<Text>', 'outfile.mp3')
    sys.exit(1)

text = sys.argv[1]
filename = sys.argv[2]
# The text that you want to convert to audio
mytext = text
  
# Language in which you want to convert
language = 'en'
  
# Passing the text and language to the engine, 
# here we have marked slow=False. Which tells 
# the module that the converted audio should 
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)
  
# Saving the converted audio in a mp3 file named
myobj.save(filename) # test.mp3

# modify pitch as speed of video will be increased
sound = AudioSegment.from_file(filename, format=filename[-3:])
octaves = -1

new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
hipitch_sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
hipitch_sound = hipitch_sound.set_frame_rate(44100)
#export / save pitch changed sound
hipitch_sound.export(filename, format="mp3")

# Playing the converted file