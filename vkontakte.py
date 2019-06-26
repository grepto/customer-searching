import os
import datetime
import time

import requests

from utils import get_filtered_list

VK_TOKEN = os.getenv('VK_TOKEN')
VK_GROUP_DOMAIN = os.getenv('VK_GROUP_DOMAIN')
DATE_LIMIT = int(os.getenv('VK_DATE_LIMIT'))

VK_API_VERSION = 5.95
VK_API_URL = 'https://api.vk.com/method'

PAYLOADS = {
    'access_token': VK_TOKEN,
    'v': VK_API_VERSION,
    'domain': VK_GROUP_DOMAIN,
}


def request_pages(url, payloads, records_per_page=100, page_limit=0):
    params = {
        **payloads,
        'count': records_per_page,
        'offset': 0,
    }
    response_items = []
    page = 0
    while page < page_limit or not page_limit:
        response = requests.get(url, params=params)
        response.raise_for_status()
        page_data = response.json()
        if page_data.get('error'):
            time.sleep(5)
            continue
        if not page_data['response']['items']:
            break
        response_items.extend(page_data['response']['items'])
        params['offset'] += records_per_page
        page += 1
    return response_items


def get_group_id(group_name):
    method_url = f'{VK_API_URL}/groups.getById'
    params = {
        **PAYLOADS,
        'group_ids': group_name,
    }
    response = requests.get(method_url, params=params)
    response.raise_for_status()
    if response.json().get('error'):
        raise ValueError(response.json()['error']['error_msg'])
    return response.json()['response'][0]['id']


def get_posts(records_per_page=100, page_limit=0):
    method_url = f'{VK_API_URL}/wall.get'
    return request_pages(method_url, PAYLOADS, records_per_page, page_limit)


def get_post_comments(group_id, post_id, records_per_page=100, page_limit=0):
    method_url = f'{VK_API_URL}/wall.getComments'
    params = {
        **PAYLOADS,
        'owner_id': -group_id,
        'post_id': post_id,
    }
    return request_pages(method_url, params, records_per_page, page_limit)


def get_commentators(comments):
    return {comment.get('from_id') for comment in comments if comment.get('from_id') and comment.get('from_id') > 0}


def get_likers(group_id, post_id, records_per_page=100, page_limit=0):
    method_url = f'{VK_API_URL}/likes.getList'
    params = {
        **PAYLOADS,
        'type': 'post',
        'owner_id': -group_id,
        'item_id': post_id,
    }
    return request_pages(method_url, params, records_per_page, page_limit)


def get_vk_core_users():
    group_id = get_group_id(VK_GROUP_DOMAIN)
    timedelta = datetime.timedelta(days=DATE_LIMIT)
    posts = get_posts()
    commentators = []
    likers = []
    for post in posts:
        post_id = post['id']
        comments = get_post_comments(group_id, post_id)
        filtered_comments = get_filtered_list(comments, 'date', timedelta)
        commentators.extend(get_commentators(filtered_comments))
        likers.extend(get_likers(group_id, post_id))

    return set(commentators) & set(likers)


def main():
    print(get_vk_core_users())


if __name__ == '__main__':
    main()
