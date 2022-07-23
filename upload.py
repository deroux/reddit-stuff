import os

if __name__ == '__main__':   # will only run when script1.py is run directly
    videoFile = 'videos/0/final_video.mp4'
    with open("info_0.txt") as file:
        lines = file.readlines()
        lines = [el.replace('\n', '') for el in lines]
        title = lines[0]
        description = lines[1]
        keywords = lines[2]
        category = lines[3]
    
    print('python3 upload_video.py --file {v} --title {t} --description {d} --category {c} --keywords {k} --privacyStatus private'.format(
        v=videoFile, t=title, d=description, c=category, k=keywords))
    os.system('python3 upload_video.py --file {v} --title "{t}" --description "{d}" --category {c} --keywords "{k}" --privacyStatus private'.format(v=videoFile, t=title, d=description, c=category, k=keywords))
