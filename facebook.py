import datetime
from collections import defaultdict, Counter
import os

import requests

from utils import get_filtered_list


FB_URL = 'https://graph.facebook.com'
FB_TOKEN = os.getenv('FB_TOKEN')
DATE_LIMIT = int(os.getenv('FB_DATE_LIMIT'))

payloads = {
    'access_token': FB_TOKEN
}


def get_user_id():
    url = f'{FB_URL}/me'
    params = payloads
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['id']


def get_group_id(user_id):
    url = f'{FB_URL}/{user_id}/groups'
    params = payloads
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['data'][0]['id']


def get_posts(group_id):
    url = f'{FB_URL}/{group_id}/feed'
    params = payloads
    response = requests.get(url, params=params)
    response.raise_for_status()
    return [post['id'] for post in response.json()['data']]


def get_comments(post_id):
    url = f'{FB_URL}/{post_id}/comments'
    params = payloads
    params['fields'] = 'from,created_time'
    response = requests.get(url, params=params)
    response.raise_for_status()
    comments = response.json()['data']
    return [
        dict(author_id=comment['from']['id'],
             created_time=datetime.datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000').timestamp(),
             )
        for comment in comments]


def get_reactions(post_id):
    url = f'{FB_URL}/{post_id}/reactions'
    params = payloads
    params['fields'] = 'id,type'
    response = requests.get(url, params=params)
    response.raise_for_status()
    reactions = response.json()['data']
    return [(reaction['id'], reaction['type']) for reaction in reactions]


def group_reactions_by_author(reactions):
    grouped_reactions = defaultdict(list)
    for user_id, reaction in reactions:
        grouped_reactions[user_id].append(reaction)
    return grouped_reactions


def count_reactions(grouped_reactions):
    calculated_reactions = dict()
    for author, reactions in grouped_reactions.items():
        calculated_reactions[author] = dict(Counter(reactions))
    return calculated_reactions


def analyze_facebook():
    user_id = get_user_id()
    group_id = get_group_id(user_id)
    timedelta = datetime.timedelta(days=DATE_LIMIT)
    posts = get_posts(group_id)

    reactions = []
    commentators = []
    for post in posts:
        comments = get_comments(post)
        filtered_comments = get_filtered_list(comments, 'created_time', timedelta)
        commentators.extend([comment['author_id'] for comment in filtered_comments])
        reactions.extend(get_reactions(post))
    grouped_reactions = group_reactions_by_author(reactions)
    counted_reactions = count_reactions(grouped_reactions)
    print('Commentators: ', set(commentators), sep=' ')
    print()
    print('Reactions: ', counted_reactions, sep=' ')


def main():
    analyze_facebook()


if __name__ == '__main__':
    main()
