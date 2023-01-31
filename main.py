import datetime
import os
import shutil
import time
import win32gui
from PyQt5.QtWidgets import QApplication
import sys
from configUtils import conf
from dbUtils import insert_game_info
from fileUtils import delete_old_file
from imageUtils import comparison, location_player
from ocr import get_image_text_info

hwnd_title = dict()

START_AGAIN = int(conf.get("base", "start_again"))
SCREENSHOT_INTERVAL = int(conf.get("base", "screenshot_interval"))


def get_all_hwnd(hwnd, mouse):
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})


win32gui.EnumWindows(get_all_hwnd, 0)
print(hwnd_title.items())

# 程序会打印窗口的hwnd和title，有了title就可以进行截图了。
hwnd = win32gui.FindWindow(None, 'League of Legends (TM) Client')
app = QApplication(sys.argv)
screen = QApplication.primaryScreen()
img = screen.grabWindow(hwnd).toImage()

# img.save("screenshot2.jpg")
while True:
    # print("备份最新图片")
    d = datetime.datetime.today()
    dateStr = d.strftime('%Y%m%d%H%M%S')
    if os.path.exists('screenshot/latest.jpg'):
        # os.rename('screenshot/latest.jpg', 'screenshot/' + dateStr + '.jpg')
        shutil.copyfile("screenshot/latest.jpg", 'screenshot/' + dateStr + '.jpg')
    # print("正在截图")
    screen = QApplication.primaryScreen()
    hwnd = win32gui.FindWindow(None, 'League of Legends(TM)Client')
    img = screen.grabWindow(hwnd).toImage()
    latest_image_path = "screenshot/latest.jpg"
    img.save(latest_image_path)
    # 对比图片
    comparison_result = comparison(latest_image_path, "resources/target.jpg")
    print("开局相似度：", comparison_result)
    if comparison_result > 0.9:
        print("发现对局，进行对局玩家分析.....")
        # 拷贝图片到目录
        game_image_path = "gameScreenshot/" + dateStr + ".jpg"
        shutil.copyfile("screenshot/latest.jpg", game_image_path)
        # 拼接待检测图片
        location_player(game_image_path)
        result = get_image_text_info("temp/finish_image.jpg")
        insert_game_info(result)
        # win32api.MessageBox(None, "测试", "遇见熟人", win32con.MB_SYSTEMMODAL)
        time.sleep(START_AGAIN)
    delete_old_file()
    time.sleep(SCREENSHOT_INTERVAL)
