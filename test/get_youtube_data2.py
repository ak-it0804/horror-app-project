from apiclient.discovery import build
import yaml
import pandas as pd
import re
from datetime import datetime, timedelta

with open('./key.yaml', 'r') as yml:
    key_dict = yaml.safe_load(yml)


YOUTUBE_API_KEY = key_dict['YOUTUBE_API_KEY2']

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def get_video_info(part, q, order,type, num):
    dic_list = []
    search_response = youtube.search().list(part=part,q=q,order=order,type=type)
    output = youtube.search().list(part=part,q=q,order=order,type=type).execute()

    # 一度に5件しか取得できないため何度も繰り返して実行
    for i in range(num):
        dic_list = dic_list + output['items']
        search_response = youtube.search().list_next(search_response, output)
        output = search_response.execute()

    df = pd.DataFrame(dic_list)
    # 各動画ごとに一意のvideoIdを取得必要な動画情報だけ取得
    df1 = pd.DataFrame(list(df['id']))['videoId']
    # 各動画ごとに一意の種特筆ゆな動画情報だけ取得
    df2 = pd.DataFrame(list(df['snippet']))[['channelTitle','title','description','channelId']]

    ddf = pd.concat([df1,df2], axis=1)

    df_static = pd.DataFrame(list(ddf['videoId'].apply(lambda x : get_statistics(x))))

    # df_duration = pd.DataFrame(list(ddf['videoId'].apply(lambda x : get_duration(x))))

    df_output = pd.concat([ddf, df_static], axis=1)

    return df_output

def get_statistics(id):
    statistics = youtube.videos().list(part = 'statistics', id = id).execute()['items'][0]['statistics']

    return statistics


# def get_duration(id):
#     '''動画時間を抜き出す（ISO表記を秒に変換）'''
#     pt_time = youtube.videos().list(part = 'contentDetails', id = id).execute()['items'][0]['contentDetails']['duration']
#     return pt2sec(pt_time)

def pt2sec(pt_time):
    '''ISO表記の動画時間を秒に変換 '''
    pttn_time = re.compile(r'PT(\d+H)?(\d+M)?(\d+S)?')
    keys = ['hours', 'minutes', 'seconds']
    m = pttn_time.search(pt_time)
    if m:
        kwargs = {k: 0 if v is None else int(v[:-1])
                    for k, v in zip(keys, m.groups())}
        return timedelta(**kwargs).total_seconds()
    else:
        msg = '{} is not valid ISO time format.'.format(pt_time)
        raise ValueError(msg)


if __name__ == '__main__':
    video_info = get_video_info(part='snippet',q='怖い話',order='viewCount',type='video',num=30)

    print(video_info.head(5))

    video_info.to_csv('./output/horror_video_info.csv', index=False)
