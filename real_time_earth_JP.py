from PIL import Image, ImageDraw, ImageFont
from time import sleep
import win32con
import win32gui
import win32api
import requests
import datetime
import re
import os
# 屏幕分辨率
X = int(win32api.GetSystemMetrics(win32con.SM_CXSCREEN) * 1.5)
Y = int(win32api.GetSystemMetrics(win32con.SM_CYSCREEN) * 1.5)
# 存储路径
path = 'D://'
name = 'wallpaper.png'


def download(url, path):
    img = requests.get(url)
    with open(path, "wb") as fwi:
        fwi.write(img.content)
        # print("下载成功")


def fill_img(path):
    global X, Y  # 屏幕分辨率

    img = Image.open(path)
    new_img = Image.new(img.mode, (X, Y), color='black')
    new_img.paste(img, (int(X / 2 - 250), int(Y / 2 - 250)))
    new_img.save(path)
    # print("合成成功")


def set_wallpaper(path):
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                              "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, path, 1 + 2)


def get_time_path():
    global today, path_today

    today = datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
    path_today = today.strftime("%Y/%m/%d/%H%M")
    path_today_list = list(path_today)
    path_today_list[-1] = "0"
    path_today = "".join(path_today_list)


def get_time():
    return datetime.datetime.utcnow()


def main():
    global today, path_today, path, name

    get_time_path()
    url = f"https://himawari8-dl.nict.go.jp/himawari8/img/D531106/1d/550/{path_today}00_0_0.png"
    download(url, path + name)
    fill_img(path + name)


def draw_time():
    global today, path_today, path, name
    global X, Y

    img = Image.open(path+name)
    draw = ImageDraw.Draw(img)
    # 画圆
    draw.arc((X - 390, 120, X - 110, 400), 0, 360, fill=(255, 255, 255))
    draw.arc((X - 389, 121, X - 111, 399), 0, 360, fill=(255, 255, 255))
    draw.arc((X - 388, 122, X - 112, 398), 0, 360, fill=(255, 255, 255))
    draw.arc((X - 387, 123, X - 113, 397), 0, 360, fill=(255, 255, 255))
    draw.arc((X - 386, 124, X - 114, 396), 0, 360, fill=(255, 255, 255))
    a = int(get_time().strftime("%H")) + 8
    a = '%02d' % a
    # 在图片上打印时间
    draw.text((X-360, 200), f'{a}\'{get_time().strftime("%M")}',
              fill=(255, 255, 255), font=ImageFont.truetype('arial.ttf', 90))
    draw.text((X-310, 300), f'{get_time().strftime("%b")}.{get_time().strftime("%d")}',
              fill=(255, 255, 255), font=ImageFont.truetype('arial.ttf', 40))
    img.save(path + '_' + name)


if __name__ == '__main__':
    if os.system('ping www.baidu.com') == 0:
        main()
    if os.path.exists(path + name):
        draw_time()
        set_wallpaper(path + '_' + name)
    else:
        (Image.new('RGB', (X, Y), color='black')).save(path+name)
    num = 0
    temp = '0'
    while (1):
        if num >= 10 and os.system('ping www.baidu.com') == 0:
            num = 0
            main()
            draw_time()
            set_wallpaper(path + '_' + name)
            print('123')
            sleep(55)
        if get_time().strftime('%M') != temp:
            num += 1
            temp = get_time().strftime('%M')
            draw_time()
            set_wallpaper(path + '_' + name)
            sleep(55)
