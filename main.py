import datetime
import os
import subprocess
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
    subprocess.Popen('gsettings set org.gnome.desktop.background picture-uri ' + full_path, shell=True)
    time.sleep(2)
    # 更换锁屏
    subprocess.Popen('convert -blur 0x25 ~/.cache/wallpaper/* ~/Pictures/gdmlock.jpg', shell=True)
    time.sleep(3)
    subprocess.Popen('cp -f ~/Pictures/gdmlock.jpg /usr/share/backgrounds/', shell=True)


if __name__ == '__main__':
    file_name = datetime.date.today().strftime('%y%m%d') + '.jpg'
    file = os.path.expanduser('~/Pictures/Wallpapers/' + file_name)
    if not os.path.exists(file):
        picture_url = get_picture_url()
        download_picture(picture_url, file)
    change_wallpaper(file)
