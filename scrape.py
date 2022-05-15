
import praw
import pandas as pd
from praw.models import MoreComments
import re

def FindURL(string):  
    return ('http' in string)

# Read-only instance
reddit_read_only = praw.Reddit(client_id="01KNcwq8-vLPPQqSdw4Smg",         # your client id
                               client_secret="hSC7hv8z6MfBoKultJCPNXgqZw5ydA",      # your client secret
                               user_agent="exp3ctopatr0num")        # your user agent
 

sub = ['Facepalm', 'Askreddit']  # make a list of subreddits you want to scrape the data from

subs = {}
for s in sub:
    subreddit = reddit_read_only.subreddit(s)   # Chosing the subreddit

########################################
#   CREATING DICTIONARY TO STORE THE DATA WHICH WILL BE CONVERTED TO A DATAFRAME
########################################

#   NOTE: ALL THE POST DATA AND COMMENT DATA WILL BE SAVED IN TWO DIFFERENT
#   DATASETS AND LATER CAN BE MAPPED USING IDS OF POSTS/COMMENTS AS WE WILL 
#   BE CAPTURING ALL IDS THAT COME IN OUR WAY

    MIN_SCORE_1 = 50
    MIN_SCORE_2 = 50
    MIN_SCORE_3 = 50
# SCRAPING CAN BE DONE VIA VARIOUS STRATEGIES {HOT,TOP,etc} we will go with keyword strategy i.e using search a keyword
    query = ['']
    out = {}
    # url = "das hier ist ein text https://www.reddit.com/r/funny/comments/3g1jfi/buttons/"
    for submission in subreddit.hot(limit=2): #subreddit.search(query, sort = "top", limit = 1):
        # submission = reddit_read_only.submission(url=url)
        comm = {}
        comm[submission.url] = submission.score
        submission.comments.replace_more(limit=5)
        for top_level_comment in submission.comments:
            if top_level_comment.score > MIN_SCORE_1 and not FindURL(top_level_comment.body):
                obj = {}
                for second_level_comment in top_level_comment.replies:
                    if second_level_comment.score > MIN_SCORE_2 and not FindURL(second_level_comment.body):
                        obj[second_level_comment.body] = second_level_comment.score 
                #        for third_level_comment in second_level_comment.replies:
                #            if third_level_comment.score > MIN_SCORE_3 and not FindURL(third_level_comment.body):
                #                comm[third_level_comment.body] = third_level_comment.score
                comm[top_level_comment.body] = obj
    out[submission.title] = comm
    subs[s] = out
print(subs)
        # for comment in submission.comments.list():
        #    comm[comment.body] = comment.score
        
        


def normalize_body(dic):

        """
        for item in query:
        post_dict = {
            "title" : [],
            "score" : [],
            "id" : [],
            "url" : [],
            "comms_num": [],
            "created" : [],
            "body" : []
        }
        comments_dict = {
            "comment_id" : [],
            "comment_parent_id" : [],
            "comment_body" : [],
            "comment_link_id" : []
        }
        for submission in subreddit.search(query,sort = "top",limit = 1):
            post_dict["title"].append(submission.title)
            post_dict["score"].append(submission.score)
            post_dict["id"].append(submission.id)
            post_dict["url"].append(submission.url)
            post_dict["comms_num"].append(submission.num_comments)
            post_dict["created"].append(submission.created)
            post_dict["body"].append(submission.selftext)
            
            ##### Acessing comments on the post
            submission.comments.replace_more(limit = 1)
            for comment in submission.comments.list():
                comments_dict["comment_id"].append(comment.id)
                comments_dict["comment_parent_id"].append(comment.parent_id)
                comments_dict["comment_body"].append(comment.body)
                comments_dict["comment_link_id"].append(comment.link_id)
        
        post_comments = pd.DataFrame(comments_dict)


        #post_comments.to_csv(s+"_comments_"+ item +"subreddit.csv")
        #post_data = pd.DataFrame(post_dict)
        #post_data.to_csv(s+"_"+ item +"subreddit.csv")
"""