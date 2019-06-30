import os
import collections
import datetime

from instabot import Bot

from utils import get_filtered_list

LOGIN = os.getenv('INSTAGRAM_LOGIN')
PASSWORD = os.getenv('INSTAGRAM_PASSWORD')
ACCOUNT_NAME = os.getenv('INSTAGRAM_ACCOUNT_NAME')
DATE_LIMIT = int(os.getenv('INSTAGRAM_DATE_LIMIT'))


def make_bot(login, password):
    bot = Bot()
    bot.login(username=login, password=password)
    return bot


def get_comments(bot, post):
    comments = []
    for comment in bot.get_media_comments_all(post):
        comment['post_id'] = post
        comments.append(comment)
    return comments


def get_posts_filtered_comments(posts_count=None):
    bot = make_bot(LOGIN, PASSWORD)
    posts = bot.get_total_user_medias(ACCOUNT_NAME)
    comments = []
    for post in posts[0:posts_count]:
        comments.extend(get_comments(bot, post))
    timedelta = datetime.timedelta(days=DATE_LIMIT)
    return get_filtered_list(comments, 'created_at', timedelta)


def get_commentators_rate_comments(comments):
    commentators_rate = collections.Counter([comment['user_id'] for comment in comments])
    return dict(commentators_rate.most_common())


def get_commentators_rate_posts(comments):
    commentators = {(comment['user_id'], comment['post_id']) for comment in comments}
    commentators_rate = collections.Counter([user_id for user_id,  post_id in commentators])
    return dict(commentators_rate.most_common())


def main():
    comments = get_posts_filtered_comments(2)
    top_comments = get_commentators_rate_comments(comments)
    top_posts = get_commentators_rate_posts(comments)
    print(top_comments)
    print(top_posts)


if __name__ == '__main__':
    main()
