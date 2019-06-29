import argparse

from facebook import get_facebook_core_users
from vkontakte import get_vk_core_users
from instagram import get_posts_filtered_comments, get_commentators_rate_comments, get_commentators_rate_posts

parser = argparse.ArgumentParser(
    description='Получение ядра аудитории в социальных сетях Facebook, Instagram, Vkontakte'
)
parser.add_argument('network', help='Название соцсети', choices=['instagram', 'vk', 'facebook'])
args = parser.parse_args()

if args.network == 'instagram':
    comments = get_posts_filtered_comments(2)
    top_comments = get_commentators_rate_comments(comments)
    top_posts = get_commentators_rate_posts(comments)
    print('Comments Top:', top_comments, sep=' ')
    print('Posts Top:', top_posts, sep=' ')

elif args.network == 'vk':
    print(get_vk_core_users())
elif args.network == 'facebook':
    for rate_type, users in get_facebook_core_users().items():
        print(rate_type, users, sep=' ', end='\n\n')
