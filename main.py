import datetime
import os
import time

import requests


def get_picture_url():
    url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&nc=1546870370143&pid=hp&video=1'
    res = requests.get(url)
    if res.status_code == 200:
        result = res.json()
        return 'https://cn.bing.com' + result['images'][0]['url']


def download_picture(url, path):
    res = requests.get(url)
    if res.status_code == 200:
        try:
            with open(path, 'bx') as f:
                f.write(res.content)
        except Exception:
            return


def change_wallpaper(path):
    # 更换壁纸
    full_path = 'file://' + path
    os.system('gsettings set org.gnome.desktop.background picture-uri ' + full_path)
    time.sleep(2)
    # 更换锁屏
    os.system('convert -blur 0x25 ~/.cache/wallpaper/* ~/Pictures/gdmlock.jpg')
    time.sleep(3)
    os.system('cp -f ~/Pictures/gdmlock.jpg /usr/share/backgrounds/')


if __name__ == '__main__':
    picture_url = get_picture_url()
    file = os.path.expanduser('~/Pictures/Wallpapers/' + datetime.date.today().strftime('%y%m%d') + '.jpg')
    download_picture(picture_url, file)
    change_wallpaper(file)
