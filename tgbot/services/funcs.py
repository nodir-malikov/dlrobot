from __future__ import unicode_literals

import logging
import re
from urllib import parse
import youtube_dl

from tgbot.config import load_config

config = load_config()


async def youtube_download(link: str):
    video_id = await yt_video_id(link)

    async def progress_hook(d):
        if d['status'] == "downloading":
            logging.info(f'{d["_speed_str"]({d["_percent_str"]})}')
        else:
            logging.info('Tayyor!')

    ydl_opts = {
        'format': '[filesize<100M]',
        'progress_hook': [progress_hook],
        'outtmpl': f'{config.tg_bot.yt_path}%(extractor)s-%(id)s-%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])
    return video_id


async def find_url(string: str):
    # findall() has been used
    # with valid conditions for urls in string
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)" \
            r"(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!(" \
            r")\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, string)
    return [x[0] for x in url]


async def yt_video_id(link):
    """
    Examples:
    - http://youtu.be/SA2iWivDJiE
    - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    - http://www.youtube.com/embed/SA2iWivDJiE
    - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    """
    query = parse.urlparse(link)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse.parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    # fail?
    return None
