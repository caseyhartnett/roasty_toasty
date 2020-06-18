import praw
from praw.models import MoreComments
import PIL
from PIL import Image
import requests
from io import BytesIO
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
import pandas as pd
from sys import argv


class Scraper:
    def __init__(self, subreddit=None, limit=5):
        self.reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                                  client_secret=REDDIT_CLIENT_SECRET,
                                  user_agent=REDDIT_USER_AGENT)
        self.subreddit = subreddit
        self.extract_top_posts(limit)

    def extract_top_posts(self, limit):
        top_posts = self.reddit.subreddit(self.subreddit).top(limit=limit)
        all_comments = list()
        for post in top_posts:
            try:
                img = extract_image(post)
                img.save(f"data/images/{self.subreddit}/{post.id}.jpg", "JPEG",
                         quality=80, optimize=True, progressive=True)
                all_comments.extend(extract_comments(post))
            # handle when image is not identifiable/usable
            except PIL.UnidentifiedImageError:
                print(f"An error occurred for post [{post.id}]")
                continue
        pd.DataFrame(all_comments).to_csv(f'data/top_posts_{self.subreddit}.csv')


def extract_comments(post):
    comments = list()
    for top_level_comment in post.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        comment_dict = {'post_id': post.id,
                        'comment_score': top_level_comment.score,
                        'comment_body': top_level_comment.body}
        comments.append(comment_dict)
    return comments


def extract_image(post):
    response = requests.get(post.url)
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGB")
    return img


if __name__ == '__main__':
    subreddit = argv[1]
    limit = int(argv[2])
    Scraper(subreddit, limit)
