import datetime
from collections import defaultdict, Counter
import os

import requests

from utils import get_filtered_list

FB_URL = 'https://graph.facebook.com'
FB_TOKEN = os.getenv('FB_TOKEN')
DATE_LIMIT = int(os.getenv('FB_DATE_LIMIT'))

PAYLOADS = {
    'access_token': FB_TOKEN
}


def get_user_id():
    url = f'{FB_URL}/me'
    params = PAYLOADS
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['id']


def get_group_id(user_id):
    url = f'{FB_URL}/{user_id}/groups'
    params = PAYLOADS
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()['data'][0]['id']


def get_post_ids():
    user_id = get_user_id()
    group_id = get_group_id(user_id)
    url = f'{FB_URL}/{group_id}/feed'
    params = PAYLOADS
    response = requests.get(url, params=params)
    response.raise_for_status()
    return [post['id'] for post in response.json()['data']]


def get_comments(post_id):
    url = f'{FB_URL}/{post_id}/comments'
    params = {
        **PAYLOADS,
        'fields': 'from,created_time',
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    comments = response.json()['data']
    return [
        dict(author_id=comment['from']['id'],
             created_time=datetime.datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000').timestamp(),
             )
        for comment in comments]


def get_commentators(post_ids):
    timedelta = datetime.timedelta(days=DATE_LIMIT)
    commentators = set()
    for post_id in post_ids:
        comments = get_comments(post_id)
        filtered_comments = get_filtered_list(comments, 'created_time', timedelta)
        commentators.update([comment['author_id'] for comment in filtered_comments])
    return commentators


def get_reactions(post_id):
    url = f'{FB_URL}/{post_id}/reactions'
    params = {
        **PAYLOADS,
        'fields': 'id,type',
    }
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


def get_counted_reactions(post_ids):
    reactions = [reaction for post_id in post_ids for reaction in get_reactions(post_id)]
    grouped_reactions = group_reactions_by_author(reactions)
    return count_reactions(grouped_reactions)


def main():
    post_ids = get_post_ids()
    commentators = get_commentators(post_ids)
    counted_reactions = get_counted_reactions(post_ids)
    print('Commentators:', commentators, sep=' ')
    print('Reactions:', counted_reactions, sep=' ')


if __name__ == '__main__':
    main()
