from apiclient.discovery import build
import yaml

with open('./key.yaml', 'r') as yml:
    key_dict = yaml.safe_load(yml)

videoId = '6RLhVKmwraM'
YOUTUBE_API_KEY = key_dict['YOUTUBE_API_KEY']

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
videos_response = youtube.videos().list(
    part='snippet,statistics',
    id='{},'.format(videoId)
).execute()
# snippet
snippetInfo = videos_response["items"][0]["snippet"]
# 動画タイトル
title = snippetInfo['title']
# チャンネル名
channeltitle = snippetInfo['channelTitle']
print(channeltitle)
print(title)