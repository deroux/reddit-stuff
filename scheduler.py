# Watch file system, if textfiles && sounds && videos folder is empty, scrape subbreddits

# Every 3 hours during the day, select random final_video from videos and upload, afterwards delete folder

import os

from apscheduler.schedulers.blocking import BlockingScheduler


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def directoryIsEmpty(path):
    return len(os.listdir(path)) == 0


def scrapeReddit(subreddit, interval):
    os.system('python3 scrapeReddit.py "{subreddit}" "{interval}"'.format(
        subreddit=subreddit, interval=interval))

sched = BlockingScheduler()
subreddits = ['AskReddit',
              'worldnews',
              'science',
              'movies',
              'todayilearned',
              'news',
              'Showerthoughts',
              'Jokes',
              'askscience',
              'IAmA',
              'books',
              'explainlikeimfive',
              'LifeProTips',
              'Futurology',
              'NatureIsFuckingLit',
              'Fitness',
              'tifu',
              'PoliticalHumor']

i = 0

@sched.scheduled_job('interval', minutes=5)
def check_data_available():
    print(f"{bcolors.OKCYAN} Checking data available for upload ... {bcolors.ENDC}")
    if (directoryIsEmpty('textfiles') and directoryIsEmpty('sounds') and directoryIsEmpty('videos') and directoryIsEmpty('infofiles')):
        # everything has been uploaded, need to re-scrape
        if (i < len(subreddits)):
            sub = subreddits.pop(0)
            print(f"{bcolors.WARNING} Scraping subreddit '{sub}' for 'week'... {bcolors.ENDC}")
            scrapeReddit(sub, 'week')
        else:
            i = 0
    else:
        print(len(subreddits))
        print(
            f"{bcolors.OKGREEN} Still {len(os.listdir('videos'))} videos left for upload ... {bcolors.ENDC}")

# from 5 to 21 every 3 hours, e.g. 5:45, 8:45, 11:45, 14:45, 17:45, 20:45
# @sched.scheduled_job('cron', hour='5-21/3', minute=45)
# @sched.scheduled_job('cron', hour='11', minute=35)
@sched.scheduled_job('cron', hour='5-21/3', minute=47)
def upload_video():
    # get first directory in videos folder
    folders = os.listdir('videos')
    if ('.DS_Store' in folders):
        folders.remove('.DS_Store')

    if (len(folders)==0):
        print(f"{bcolors.FAIL} No upload possible: no folders available... {bcolors.ENDC}")
    else:
        folder = folders[0]
        print(f"{bcolors.OKGREEN} uploading video /{folder}/final_video.mp4 ... {bcolors.ENDC}")
        video_path = f'videos/{folder}/final_video.mp4'
        # upload video, uploads thumbnail, deletes folder and all data afterwards
        # upload.py /videos/0/final_video.mp4
        os.system('python3 upload.py "{video}"'.format(video=video_path))





# sched.configure(options_from_ini_file)
sched.start()
