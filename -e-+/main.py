# 此文件用于测试功能

# import tensorflow as tf
import numpy as np
import cv2

import attitude
import identify
import predict

attitude_net = attitude.attitude()
capture = identify.capture()

net = predict.predict_cnn
# net = predict.predict_dnn

cap = cv2.VideoCapture(0)

def image(image):
    # is_violation = False
    is_violation = net(image)
    print(is_violation)
    # Save the picture to the database
    if is_violation:
        pass


def video():
    b_was_show_tip = False
    is_violation = False
    while True:
        # 读取摄像头中的这一帧
        ret, frame = cap.read()
        if not ret:
            print("摄像头出错")
            cap.release()
            break
        is_violation = net(frame)
        print(is_violation)
        # Save the picture to the database
        if is_violation:
            pass





def main():

    mode = "image"  # video/image
    # mode = "video"  # video/image
    # mode = "test"

    if mode == "image":
        im = cv2.imread("images/5_0.jpg")
        image(im)
        cv2.waitKey(0)

    elif mode == "video":
        video()




main()
