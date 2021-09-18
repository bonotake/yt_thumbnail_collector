import argparse
import csv
from datetime import datetime, timezone, timedelta
from glob import glob
from google.oauth2 import service_account
from pathlib import Path
from typing import List, Optional
from zoneinfo import ZoneInfo

from thumbnail_collector import get_video_infos, download_thumbnails


CREDENTIAL_FILE = './google-credentials.json'
VIDEO_INFO_LIST_FILE = 'data/video_id_list.txt'
VIDEO_INFO_CSV_FILE = 'data/mito_archives.csv'
IMAGE_DIR_PATH = 'data/images'

# Mito's Channel ID
HIKAKIN_CHANNEL_ID = "UCZf__ehlCEBPop-_sldpBUQ"


def get_default_date() -> datetime:
    return datetime.today() - timedelta(days=10)


def main(channel_id: Optional[str], since: Optional[str]) -> None:
    video_info_list_file = Path(VIDEO_INFO_LIST_FILE)
    if not video_info_list_file.exists():
        credentials =\
            service_account.Credentials.from_service_account_file(CREDENTIAL_FILE)

        # set channel and date
        our_channel_id = HIKAKIN_CHANNEL_ID if channel_id is None else channel_id
        start_date = get_default_date() if since is None \
            else datetime.strptime(since, '%Y/%m/%d')
        start_date = start_date.astimezone()  # set local timezone
        start_date = start_date.astimezone(timezone.utc)  # set 

        # check the latest video
        date_str = start_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        print(date_str)
        videoInfos = get_video_infos(credentials, 
            channel_id=our_channel_id,
            since_date=date_str)

        # output videoID list to intermediate file
        videoStrs = [f'{info[0]}, {info[1]}' for info in videoInfos]
        infos_str = '\n'.join(videoStrs)
        with open(video_info_list_file, 'w') as f:
            f.write(infos_str)

    else:
        with open(video_info_list_file) as f:
            videoStrs = f.read().splitlines()

    tmp = map(lambda s: s.split(','), videoStrs)
    videoInfos = [(info[0], info[1]) for info in tmp]

    # download
    print('start downloading...')
    download_thumbnails(videoInfos, IMAGE_DIR_PATH)
    print('done')



if __name__ == '__main__':
    # arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--channel', help='specify YouTube Channel ID')
    parser.add_argument('--since', help='specify the starting date ex. "2021/09/18"')
    args = parser.parse_args()

    main(channel_id=args.channel, since=args.since)
