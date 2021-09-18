import requests
import time
from typing import List, Tuple


def download_thumbnails(info_list: List[Tuple[str, str]], dir: str, since: int = 0) -> None:
    for id, date in info_list:
        filename = f'{dir}/{date}.jpg'
        url = f'http://img.youtube.com/vi/{id}/maxresdefault.jpg'
        print(f'download {date}')
        data = requests.get(url).content
        with open(filename, 'wb') as f:
            f.write(data)

        # sleep
        time.sleep(0.5)
