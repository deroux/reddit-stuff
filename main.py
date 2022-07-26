import json
import math
import os
import re
import sys
from concurrent.futures import process

from moviepy.editor import *


def FindURLs(string):
    # findall() has been used 
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex,string)      
    return [x[0] for x in url]

def scrape():
    os.system('python3 scrapeHottest.py')

def scrapeReddit(subreddit, interval):
    os.system('python3 scrapeReddit.py "{subreddit}" "{interval}"'.format(subreddit=subreddit, interval=interval))

def normalize_text_for_tts(text):
    # only necessary for tts
    # append point to end of line as otherwise TTS might get confused, compare... I was kidnapped. AMA without point
    if '<3' in text:
        text = text.replace('<3', '')
    text = text.strip()
    if not (text.endswith('.') or text.endswith('?') or text.endswith('!')):
        text = text + '.'

    # tts has problems with multiple points
    while '..' in text:
        text = text.replace('..', '.')

    text = text.strip()
    text = text.replace(' bc ', ' because ')
    text = text.replace(':)', '')
    text = text.replace(';)', '')
    text = text.replace(':,)', '')
    # many times it is something like advice/experience
    text = text.replace('-', '.')
    text = text.replace('/', ' or ')
    text = text.replace(':', '.')
    text = text.replace('. ', '.')
    text = text.replace('.', '. ')
    text = text.replace(',.', '. ')
    text = text.replace('.,.', '. ')
    text = text.replace(' \'', ' ')  # can't handle apostrophes
    text = text.replace('\' ', ' ')  # can't handle apostrophes
    text = text.strip()

    while '?!' in text:
        text = text.replace('?!', '?')
    while '..' in text:
        text = text.replace('..', '.')
    while '\\' in text:
        text = text.replace('\\', '')
    while '/' in text:
        text = text.replace('/', '')
    while '*' in text:
        text = text.replace('*', '')
    while '??' in text:
        text = text.replace('??', '?')
    while '!!' in text:
        text = text.replace('!!', '!')
    while '>' in text:
        text = text.replace('>', '')
    while '<' in text:
        text = text.replace('<', '')
    while '=' in text:
        text = text.replace('=', '')
    while '&' in text:
        text = text.replace('&', '')
    while '_' in text:
        text = text.replace('_', '')

    # add proper commas
    text = text.replace(', ', ',')
    text = text.replace(',', ', ')
    text = text.replace('. .', '.')
    return text

def get_all_scraped_textfiles():
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
    #try:
    iterate_recursion_comments(data['comments'], processing_text)
    #except Exception as e:
    ##    print('Something went wrong with file..' + file)
    #    print(e)
    #    sys.exit(1)
        
    return processing_text

def iterate_recursion_comments(data, texts):
    for key in data.keys():
        el = data[key]
        if ('body' in el):
            if (isinstance(el, dict)):
                body = el.get('body')
            else:
                body = el
            # maybe move this check to scraping from reddit script
            if (len(FindURLs(body)) == 0):
                texts.append(body)
                if (isinstance(el, dict)):
                    if ('comments' in el) and (el.get('comments')):
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
    # just for gTTS
    # final = final_video.fx(vfx.speedx, 2)

    # final_video.set_audio(concatenate_audioclips(audios))
    final_video.write_videofile("videos/{a}/final_video.mp4".format(
        a=a), codec='libx264', audio_codec='aac', fps=10, remove_temp=True)

def cleanup(a):
    path = "sounds/{a}".format(a=a)
    os.system('rm -rf {path}'.format(path=path))

if __name__ == '__main__':   # will only run when script1.py is run directly
    # scrape();
    # scrapeReddit('ama', 'week')

    # get all scraped text files
    files = get_all_scraped_textfiles()

    a = -1
    for file in files:
        # hottest_0.json
        a = file.split('/')[1]
        a = a.split('_')[1]
        a = a.split('.')[0]
        print(a)
        print('processing... ' + file)
        # get array with text body data from file content
        file_content = []
        file_content = get_file_content(file)
        
        processing_text = []
        for text in file_content:
            go = True
            txt = text
            n = 800

            if (len(txt) <= n):
                processing_text.append(txt)
            else:
                while(len(txt) > n):
                    n = 700
                    split = len(txt)
                    while (split > n):
                        split = math.ceil(split / 2)

                    while(txt[split] != ' '): # we dont want half cutted words
                        if (len(txt) > split + 1):
                            split += 1
                        else: 
                            break

                    part = txt[:split]
                    txt = txt[split:]
                    processing_text.append(part)
                processing_text.append(txt)

        # create audio files
        i = 0
        path = "sounds/{a}".format(a=a)

        if (os.path.exists(path) == False):
            os.mkdir(path)
        
        files_re_check = []
        if (len(processing_text) > 100):
            processing_text = processing_text[0:99]
        for text in processing_text:
            soundsFile = "sounds/{a}/_{i}.mp3".format(a=a, i=i)
            if os.path.exists(soundsFile):
                #print(soundsFile)
                #print('sounds file existing ... skipping')
                i = i + 1
                continue
            text = normalize_text_for_tts(text)
            #print('text_to_speech... ' + file + " ...sounds/{a}/_{i}.mp3".format(a=a, i=i))
            os.system('python3 text_to_speech.py \"{text}\" "sounds/{a}/_{i}.mp3"'.format(text=text, a=a, i=i))

            if os.path.exists(soundsFile):
                # check if file size is huge, something might have gone wrong
                print(len(text)*1024*10)
                print(os.path.getsize(soundsFile))
                if (len(text)*1024*10 < os.path.getsize(soundsFile)):
                    files_re_check.append(soundsFile)
                    print('SDKLFSDJKFDSFKLSFSDJKL')

                while (os.path.getsize(soundsFile) > 1024*1024*5): # problem when bigger than 5 MB probably
                    # retry
                    os.system(
                        'python3 text_to_speech.py \"{text}\" "sounds/{a}/_{i}.mp3"'.format(text=text, a=a, i=i))

                # print(soundsFile)
                # print('sounds file existing ... skipping')
                i = i + 1
            continue
        
        # render video with audio files
        i = 0
        path = "videos/{a}".format(a=a)
        if (os.path.exists(path) == False):
            os.mkdir(path)
        
        videos = []
        for text in processing_text:
            # print('creating part videos... ' + file)
            video_name = "videos/{a}/_{i}.mp4".format(a=a, i=i)
            if os.path.exists(video_name):
                # print('video file existing ... skipping')
                videos.append(video_name)
                i = i + 1
                continue
            
            os.system('python3 video.py \"{text}\" "sounds/{a}/_{i}.mp3" "videos/{a}/_{i}.mp4"'.format(text=text, a=a, i=i))

            if (os.path.exists(video_name)):
                videos.append(video_name)
                i = i + 1
        
        merge_videos(videos, a)

        # cleanup(a)
        print('done...')
        print(files_re_check)
        

