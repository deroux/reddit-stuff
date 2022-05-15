import praw
import pandas as pd
from praw.models import MoreComments
import re
import json

DEBUG = 0

def normalize_text(text):
    text = text.replace('\n\n', '')
    text = text.replace('\r', '')
    text = text.replace('\n', '')
    text = text.replace('\u2019', '\'')
    text = text.replace('\"', '\'')

    # remove unicode
    string_encode = text.encode("ascii", "ignore")
    string_decode = string_encode.decode()
    return string_decode

reddit = praw.Reddit(client_id="01KNcwq8-vLPPQqSdw4Smg",         # your client id
                               client_secret="hSC7hv8z6MfBoKultJCPNXgqZw5ydA",      # your client secret
                               user_agent="exp3ctopatr0num")        # your user agent

# posts = {}
# hot_posts = reddit.subreddit('ama').hot(limit=1)
LIMIT_SCORE = 50
LIMIT_SCORE_COMMENTS_LEVEL1 = 5
LIMIT_SCORE_COMMENTS_LEVEL2 = 5

posts = {}
print('scraping top AMAs for this week...')
ama_subreddit = reddit.subreddit('ama')
for post in ama_subreddit.top('week'):
    if (post.score < LIMIT_SCORE):
        continue

    p = {}
    p['score'] = post.score
    p['title'] = normalize_text(post.title)
    p['selftext'] = normalize_text(post.selftext)
    p['url'] = post.url

    # get top level comments
    submission = reddit.submission(id=post.id)
    submission.comments.replace_more(limit=0)
    comments = {}
    for top_level_comment in submission.comments:
        if (top_level_comment.score >= LIMIT_SCORE_COMMENTS_LEVEL1):
            obj = {}
            comm = {}
            for seconds_l_c in top_level_comment.replies:
                if (seconds_l_c.score >= LIMIT_SCORE_COMMENTS_LEVEL2):
                    comm[seconds_l_c.id] = normalize_text(seconds_l_c.body)  
            obj['body'] = normalize_text(top_level_comment.body)
            obj['comments'] = comm
            comments[top_level_comment.id] = obj
    p['comments'] = comments

    # stire in posts object under id
    posts[post.id] = p
    # posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
if DEBUG:
    print(posts)

i = 0
for postId in posts:
    post = posts[postId]
    json_object = json.dumps(post, indent = 4)
    filename = "textfiles/hottest_" + str(i) + ".json"
    with open(filename, "w") as outfile:
        outfile.write(json_object)
        print("written.. " + filename)
    i = i + 1
# https://docs.aws.amazon.com/polly/latest/dg/SynthesizeSpeechSamplePython.html

