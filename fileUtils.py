import os
from configUtils import conf

RETAIN_SCREENSHOT_NUMBER = int(conf.get("base", "retain_screenshot_number"))
SCREENSHOT_INTERVAL = int(conf.get("base", "screenshot_interval"))


def delete_old_file():
    file_list = os.listdir("screenshot")
    file_list.sort()
    if len(file_list) > RETAIN_SCREENSHOT_NUMBER:
        for i in range(0, len(file_list) - RETAIN_SCREENSHOT_NUMBER):
            if str(file_list[i]) != "latest.jpg":
                file_path = "screenshot/" + str(file_list[i])
                print("清除历史截图", file_path)
                os.remove(file_path)


if __name__ == '__main__':
    delete_old_file()
