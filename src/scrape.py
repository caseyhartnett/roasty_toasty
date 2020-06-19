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
        """
        Scraping utility for subreddit data collection.
        Collects top posts and comments from given subreddit till limit is reached.

        :param subreddit: subreddit to collect data. Expect 'roastme' or toastme' but others can be used.
        :param limit: number of top posts to collect.
        """
        self.limit = limit
        self.reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                                  client_secret=REDDIT_CLIENT_SECRET,
                                  user_agent=REDDIT_USER_AGENT)
        self.subreddit = subreddit
        self.extract_top_posts()

    def extract_top_posts(self):
        """
        Extract the top posts for subreddit images and comments.
        :return: Nothing.
        """
        top_posts = self.reddit.subreddit(self.subreddit).top(limit=self.limit)
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


def extract_comments(post: praw.models.Submission) -> list:
    """
    Extract comments from a post into a dictionary for storage.
    :param post: a subreddit post to have information extracted
    :return: a list of dictionaries with `post_id`, `comment_score` and `comment_body` as keys.
    """
    comments = list()
    for top_level_comment in post.comments:
        if isinstance(top_level_comment, MoreComments):
            continue
        comment_dict = {'post_id': post.id,
                        'comment_score': top_level_comment.score,
                        'comment_body': top_level_comment.body}
        comments.append(comment_dict)
    return comments


def extract_image(post: praw.models.Submission) -> Image:
    """
    Extract the image from a post for storage
    :param post: a subreddit post to have information extracted
    :return: an Image object.
    """
    response = requests.get(post.url)
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGB")
    return img


if __name__ == '__main__':
    Scraper(argv[1], int(argv[2]))
