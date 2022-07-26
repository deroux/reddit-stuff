import os

from moviepy.editor import *  # NOTES:- PLEASE install this moviepy module
from PIL import Image


def create_thumbnail(video):
    clips = VideoFileClip(video)
    frame = clips.get_frame(1)
    new_img_file = "thumbnail.jpg"
    new_img = Image.fromarray(frame)
    new_img.save(new_img_file)
    return new_img_file

# upload.py /videos/0/final_video.mp4
if __name__ == '__main__':   # will only run when script1.py is run directly
    n = len(sys.argv)
    if (n != 2):
        print("\nCall script like:", sys.argv[0], '<Video>')
        sys.exit(1)

    videoFile = sys.argv[1]
    i = videoFile.split('/')[1]
    thumbnail = create_thumbnail(videoFile)
    with open("infofiles/info_{i}.txt".format(i=i)) as file:
        lines = file.readlines()
        lines = [el.replace('\n', '') for el in lines]
        title = lines[0]
        description = lines[1]
        keywords = lines[2]
        category = lines[3]
    
    # upload video
    os.system('python3 upload_video.py --file {v} --title "{t}" --description "{d}" --category {c} --keywords "{k}" --privacyStatus public'.format(v=videoFile, t=title, d=description, c=category, k=keywords))
    # upload thumbnail
    # os.system('python3 upload_thumbnail.py {id} {th}'.format(id=id, th=thumbnail))
