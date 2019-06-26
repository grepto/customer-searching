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


def get_commentators_rate_comments(comments):
    commentators_rate = collections.Counter()
    for comment in comments:
        commentators_rate[comment['user_id']] += 1
    return dict(commentators_rate.most_common())


def get_commentators_rate_posts(comments):
    commentators = {(comment['user_id'], comment['post_id']) for comment in comments}
    commentators_rate = collections.Counter()
    for user_id, _ in commentators:
        commentators_rate[user_id] += 1
    return dict(commentators_rate.most_common())


def analyze_instagram():
    bot = make_bot(LOGIN, PASSWORD)
    timedelta = datetime.timedelta(days=DATE_LIMIT)
    posts = bot.get_total_user_medias(ACCOUNT_NAME)
    comments = []
    for post in posts[:2]:
        comments.extend(get_comments(bot, post))
    filtered_comments = get_filtered_list(comments, 'created_at', timedelta)
    commentators_rate_comments = get_commentators_rate_comments(filtered_comments)
    commentators_rate_posts = get_commentators_rate_posts(filtered_comments)
    print('Comments Top:', commentators_rate_comments, sep=' ')
    print()
    print('Posts Top:', commentators_rate_posts, sep=' ')


def main():
    return analyze_instagram()


if __name__ == '__main__':
    main()
