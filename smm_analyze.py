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
    analyze_instagram()
elif args.network == 'vk':
    analyze_vkontakte()
elif args.network == 'facebook':
    analyze_facebook()
