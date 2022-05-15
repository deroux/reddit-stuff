from concurrent.futures import process
import os
import sys
import json
from moviepy.editor import *
import re

def FindURLs(string):
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]

def scrape():
    os.system('python3 scrapeHottest.py')

def get_all_textfiles():
    path = 'textfiles'
    list_of_files = []

    for root, dirs, files in os.walk(path):
        for file in files:
            list_of_files.append(os.path.join(root,file))
    return list_of_files

def get_file_content(file):
    with open(file) as f:
        data = json.load(f)

    processing_text = []
    processing_text.append(data['title'])
    if (data['selftext'] != ''):
        processing_text.append(data['selftext'])
    iterate_recursion_comments(data['comments'], processing_text)
    return processing_text

def iterate_recursion_comments(data, texts):
    for key in data.keys():
            
        el = data[key]
        if ('body' in el):
            # maybe move this check to scraping from reddit script
            if (len(FindURLs(el['body'])) == 0):
                texts.append(el['body'])
                iterate_recursion_comments(el['comments'], texts)
        else:
            texts.append(el)

def merge_videos(videos, a):
    print('merging videos.. ' + str(a))
    vids = []
    audios = []
    for video in videos:
        vid = VideoFileClip(video)
        vids.append(vid)
        audios.append(vid.audio)

    final_video = concatenate_videoclips(vids)
    final = final_video.fx(vfx.speedx, 2.5)

    # final_video.set_audio(concatenate_audioclips(audios))
    final.write_videofile("videos/{a}/final_video.mp4".format(a=a), codec='libx264', audio_codec='aac', fps=10, remove_temp=True)

if __name__ == '__main__':   # will only run when script1.py is run directly
    # scrape();
    # get all text files
    files = get_all_textfiles();

    # TODO: for file in files:
    file = files[0]
    print(file)

    # get array with text body data from file content
    processing_text = []
    processing_text = get_file_content(file)

    # create audio files
    a = 0
    i = 0
    path = "sounds/{a}".format(a=a)

    if (os.path.exists(path) == False):
        os.mkdir(path)
    
    for text in processing_text:
        os.system('python3 text_to_speech.py \"{text}\" "sounds/{a}/_{i}.mp3"'.format(text=text, a=a, i=i))
        i = i + 1
    
    # render video with audio files
    i = 0
    path = "videos/{a}".format(a=a)
    if (os.path.exists(path) == False):
        os.mkdir(path)
    
    videos = []
    for text in processing_text:
        video_name = "videos/{a}/_{i}.mp4".format(a=a, i=i)
        # os.system('python3 video.py \"{text}\" "sounds/{a}/_{i}.mp3" "videos/{a}/_{i}.mp4"'.format(text=text, a=a, i=i))

        if (os.path.exists(video_name)):
            videos.append(video_name)
        i = i + 1
    
    merge_videos(videos, a)
    print('done...')
        

