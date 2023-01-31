import os
import cv2
from airtest.aircv.cal_confidence import *


# 对比图片相似度
def comparison(image_path, reference_image_path):
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        return 0
    # 裁剪图片
    t = img[0:42, 0:1920]
    # 将裁剪的图片保存到临时位置
    cv2.imwrite("temp/t.jpg", t)
    temp_image_path = "temp/t.jpg"

    image = cv2.resize(cv2.imread(temp_image_path), (1920, 42))  # 图片尺寸根据实际图片写入
    target = cv2.resize(cv2.imread(reference_image_path), (1920, 42))  # 读取参考图片
    confidence = cal_ccoeff_confidence(image, target)
    # print(confidence)
    return confidence


# 拼接后，前两行是英雄名称，后两行是玩家名称
def location_player(image_path):
    img = cv2.imread(image_path)
    # 1队英雄人物
    team1_hero = img[400:422, 250:1660]
    # 2队英雄人物
    team2_hero = img[935:955, 250:1660]
    # 1队玩家名称
    team1 = img[480:500, 250:1660]
    # 2队玩家名称
    team2 = img[1015:1035, 250:1660]
    cv2.imwrite("temp/team1.jpg", team1)
    cv2.imwrite("temp/team2.jpg", team1)
    cv2.imwrite("temp/team1_hero.jpg", team1_hero)
    cv2.imwrite("temp/team2_hero.jpg", team2_hero)

    finish_image = np.vstack((team1_hero, team2_hero, team1, team2))  # hstack是横向
    cv2.imwrite("temp/finish_image.jpg", finish_image)


if __name__ == '__main__':
    # comparison("gameScreenshot/20230122114629.jpg", "resources/target.jpg")
    location_player("gameScreenshot/20230122114629.jpg")
