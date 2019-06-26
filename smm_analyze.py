import argparse

from facebook import get_facebook_core_users
from vkontakte import get_vk_core_users
from instagram import analyze_instagram

parser = argparse.ArgumentParser(
    description='Получение ядра аудитории в социальных сетях Facebook, Instagram, Vkontakte'
)
parser.add_argument('network', help='Название соцсети', choices=['instagram', 'vk', 'facebook'])
args = parser.parse_args()

if args.network == 'instagram':
    for rate_type, users in analyze_instagram().items():
        print(rate_type, users, sep=' ', end='\n\n')
elif args.network == 'vk':
    print(get_vk_core_users())
elif args.network == 'facebook':
    for rate_type, users in get_facebook_core_users().items():
        print(rate_type, users, sep=' ', end='\n\n')
