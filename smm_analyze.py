import argparse

from facebook import analyze_facebook
from vkontakte import analyze_vkontakte
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
    print(analyze_vkontakte())
elif args.network == 'facebook':
    for rate_type, users in analyze_facebook().items():
        print(rate_type, users, sep=' ', end='\n\n')
