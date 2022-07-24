import os

from moviepy.editor import *  # NOTES:- PLEASE install this moviepy module
from PIL import Image


def create_thumbnail(video, i):
    clips = VideoFileClip(video)
    frames = clips.reader.fps  # frame per second
    duration = clips.duration  # seconds

    max_duration = int(duration) + 1

    # max_duration//2 ... Get the thumbnail in middle of the video
    # You can get more thumbnails with using for loop
    frame = clips.get_frame(i)
    new_img_file = "{i}.jpg".format(i=i)

    new_img = Image.fromarray(frame)
    new_img.save(new_img_file)
    return new_img_file

if __name__ == '__main__':   # will only run when script1.py is run directly
    videoFile = 'videos/0/final_video.mp4'
    thumbnail = create_thumbnail(videoFile, 0)
    with open("info_0.txt") as file:
        lines = file.readlines()
        lines = [el.replace('\n', '') for el in lines]
        title = lines[0]
        description = lines[1]
        keywords = lines[2]
        category = lines[3]
    
    # print('python3 upload_video.py --file {v} --title {t} --description {d} --category {c} --keywords {k} --privacyStatus private'.format(
    #    v=videoFile, t=title, d=description, c=category, k=keywords))
    # os.system('python3 upload_video.py --file {v} --title "{t}" --description "{d}" --category {c} --keywords "{k}" --privacyStatus private > upload.txt'.format(v=videoFile, t=title, d=description, c=category, k=keywords))
    
    id = "ABKpMp-rFhE"
    # os.system('python3 upload_thumbnail.py {id} {th}'.format(id=id, th=thumbnail))
