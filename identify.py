# import the necessary packages
from __future__ import print_function  # 确保代码同时在Python2.7和Python3上兼容

import copy

from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils  # 安装库pip install imutils ；pip install --upgrade imutils更新版本大于v0.3.1
import cv2
from PIL import Image


class capture:

    def __init__(self):
        # construct the argument parse and parse the arguments
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-i", "--images", required=True, help="path to images directory")
        # args = vars(ap.parse_args())

        # 初始化我们的行人检测器
        self.hog = cv2.HOGDescriptor()  # 初始化方向梯度直方图描述子
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())  # 设置支持向量机(Support Vector Machine)使得它成为一个预先训练好了的行人检测器
        # OpenCV行人检测器已载入


    def get_people_location(self, image):
        # 对图片大小进行改变
        image = imutils.resize(image, width=min(500, image.shape[1]))

        image_path_list = []
        original_image = []
        b_have_people = False

        # 重新加载网络
        (rects, weights) = self.hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

        # 应用非极大抑制方法，通过设置一个阈值来抑制那些重叠的边框
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
        # print(pick)
        for (xA, yA, xB, yB) in pick:
            image_ = copy.copy(image)
            cv2.rectangle(image_, (xA, yA), (xB, yB), (0, 255, 0), 2)
            temp_save_path = "temp/temp_originally_frame.jpg"
            # 将图片写入到temp中
            cv2.imwrite(temp_save_path, image_)
            original_image = image_

        i = 0
        for (xA, yA, xB, yB) in pick:
            temp_save_path = "temp/temp" + str(i) + ".jpg"
            # 将图片写入到temp中
            cv2.imwrite(temp_save_path, image)
            # 获得要剪的区域
            box = (xA, yA, xB, yB)
            # 使用image模块打开图片并剪取
            cropImg = Image.open(temp_save_path).crop(box)
            cropImg.save(temp_save_path)  # 重新保存
            image_path_list.append(temp_save_path)  # 将这个保存的图片路径添加
            b_have_people = True
            i += 1

        # 如果图片中没有人的话
        if pick == []:
            temp_save_path = "temp/temp_no_people.jpg"
            # 将图片写入到temp中
            cv2.imwrite(temp_save_path, image)
            image_path_list.append(temp_save_path)  # 将这个保存的图片路径添加

            b_have_people = False


        # print(image_list[0])
        # cv2.waitKey(0)
        # print(image_path_list)
        return image_path_list, original_image, b_have_people


    # 测试
    def test_image(self, image):
        print(np.shape(image))
        image = imutils.resize(image, width=min(500, 700))
        print(np.shape(image))
        (rects, weights) = self.hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)
        # 应用非极大抑制方法，通过设置一个阈值来抑制那些重叠的边框
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.80)
        # print(pick)
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

        cv2.imshow("image", image)

        cv2.waitKey(0)



# capture = capture()
# image = cv2.imread("images/5_0.jpg")
# capture.test_image(image)
# image = cv2.imread("images/4_0.jpg")
# capture.test_image(image)
# image = cv2.imread("images/3_0.jpg")
# capture.test_image(image)
# print(capture.get_people_location(image))