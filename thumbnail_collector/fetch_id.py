from datetime import datetime
from pprint import pprint
from typing import List, Optional, Tuple
from googleapiclient.discovery import build

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


def oneshot(youtube, channel_id: str, since_date: str, token: Optional[str] = None) -> dict:
    kwargs = {
        'part': 'id,snippet',
        'channelId': channel_id,
        'order': 'date',
        'publishedAfter': since_date
    }
    if token is not None:
        kwargs['pageToken'] = token

    return youtube.search().list(**kwargs).execute()


def getYouTubeInfos(items: list) -> List[Tuple[str, str]]:
    return [(item['id']['videoId'], item['snippet']['publishedAt']) for item in items]

def get_video_infos(credentials, 
                    channel_id: str,
                    since_date: str) -> List[Tuple[str, str]]:
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        credentials=credentials)

    response = oneshot(youtube, channel_id, since_date)
    token = response.get('nextPageToken')    
    print('token:', token)
    items = response['items']
    videoInfos = getYouTubeInfos(items)
    for id in videoInfos:
        pprint(id)

    # if the next page exists
    while token is not None:
        print('token:', token)
        response = oneshot(youtube, channel_id, since_date, token)
        token = response.get('nextPageToken')
        items = response['items']
        new_videoInfos = getYouTubeInfos(items)
        for id in new_videoInfos:
            pprint(id)
        videoInfos += new_videoInfos

    return videoInfos
