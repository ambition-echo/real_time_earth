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
X = int(win32api.GetSystemMetrics(win32con.SM_CXSCREEN)*1.5)
Y = int(win32api.GetSystemMetrics(win32con.SM_CYSCREEN)*1.5)
path = 'D://'
name = 'wallpaper.png'
today = ''
path_today = ''


def download(url, path):
    img = requests.get(url, headers={
                       'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54'})
    with open(path, "wb") as fwi:
        fwi.write(img.content)
        # print("下载成功")


def concat_images(image_names, name, path):
    image_files = []
    for index in range(2*2):
        image_files.append(Image.open(
            path + image_names[index]))
    target = Image.new('RGB', (687 * 2, 687 * 2))

    for row in range(2):
        for col in range(2):
            target.paste(
                image_files[2*row+col], (0 + 687*col, 0 + 687*row))
    target.save(path + name, quality=100)  # 成品图保存


def fill_img(path):
    global X, Y  # 屏幕分辨率
    img = Image.open(path)
    new_img = Image.new(img.mode, (X, Y), color='black')
    new_img.paste(img, (int(X/2 - 687), int(Y/2 - 687)))
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

    today = datetime.datetime.utcnow()
    path_today = today.strftime("%Y%m%d%H%M")
    path_today = str((int(path_today)-10000)-(int(path_today) - 10000) % 100)


def get_time():
    return datetime.datetime.utcnow()


def main():
    global today, path_today, path, name

    get_time_path()
    url1 = f"http://rsapp.nsmc.org.cn/swapQuery/public/tileServer/getTile/fy-4a/full_disk/NatureColor/{path_today}00/jpg/1/0/0.png"
    url2 = f"http://rsapp.nsmc.org.cn/swapQuery/public/tileServer/getTile/fy-4a/full_disk/NatureColor/{path_today}00/jpg/1/0/1.png"
    url3 = f"http://rsapp.nsmc.org.cn/swapQuery/public/tileServer/getTile/fy-4a/full_disk/NatureColor/{path_today}00/jpg/1/1/0.png"
    url4 = f"http://rsapp.nsmc.org.cn/swapQuery/public/tileServer/getTile/fy-4a/full_disk/NatureColor/{path_today}00/jpg/1/1/1.png"
    download(url1, path + '1' + name)
    download(url2, path + '2' + name)
    download(url3, path + '3' + name)
    download(url4, path + '4' + name)

    concat_images(['1'+name, '2' + name, '3' + name, '4' + name], name, path)
    fill_img(path + name)


def draw_time():
    global today, path_today, path, name
    global X, Y

    img = Image.open(path+name)
    draw = ImageDraw.Draw(img)
    draw.arc((X-390, 120, X-110, 400), 0, 360, fill=(255, 255, 255))
    draw.arc((X-389, 121, X-111, 399), 0, 360, fill=(255, 255, 255))
    draw.arc((X-388, 122, X-112, 398), 0, 360, fill=(255, 255, 255))
    draw.arc((X-387, 123, X-113, 397), 0, 360, fill=(255, 255, 255))
    draw.arc((X-386, 124, X-114, 396), 0, 360, fill=(255, 255, 255))
    a = int(get_time().strftime("%H")) + 8
    a = '%02d' % a
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
        if num == 60 and os.system('ping www.baidu.com') == 0:
            num = 0
            main()
            draw_time()
            set_wallpaper(path + '_' + name)
            sleep(55)
        if get_time().strftime('%M') != temp:
            num += 1
            temp = get_time().strftime('%M')
            draw_time()
            set_wallpaper(path + '_' + name)
            sleep(55)
