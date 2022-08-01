import urllib.request
import os
from moviepy.editor import VideoFileClip


def task2(tiktok_url: str):
    req = urllib.request.Request(tiktok_url, headers={'User-Agent': 'XYZ/3.0'})
    tiktok_url = urllib.request.urlopen(req)

    video_name = 'Tiktok_video.mp4'
    gif_name = 'TikTok_gif.gif'
    with open(video_name, 'wb') as f:
        f.write(tiktok_url.read())
    f.close()
    video_clip = VideoFileClip(video_name).resize(0.3)
    video_clip.write_gif(gif_name, program='ffmpeg')
    return os.path.abspath(gif_name)


print(task2('https://v16-webapp.tiktok.com/6dd50826bbae87227986bf17653064ee/62e842d4/video/tos/useast2a/tos-useast2a-ve'
      '-0068c002/0b1f9147670745458190e216f0db7c66/?a=1988&ch=0&cr=0&dr=0&lr=tiktok_m&cd=0%7C0%7C1%7C0&cv=1&br=1604&bt'
      '=802&btag=80000&cs=0&ds=3&ft=ar5S8qT2mo0PD0ltVuaQ9RS1~ObpkV1PCl&mime_type=video_mp4&qs=0&rc'
      '=OzhmO2k2ZmllNWVkZzs6PEBpM2p0dGg6ZmU7ZDMzNzczM0AxMi4tYDEvNWMxLWBfYWM0YSNoYmlxcjRfYGtgLS1kMTZzcw%3D%3D&l'
      '=202208011515400102170870501138C75D'))