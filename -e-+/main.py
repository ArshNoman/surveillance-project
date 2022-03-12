# 此文件用于测试功能

import tensorflow as tf
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

def image(image, clss, u, dir):
    # is_violation = False
    is_violation = net(image)
    print(is_violation)
    # Save the picture to the database
    if is_violation:
        with open(dir, 'rb') as File:
            binary = File.read()

    db.ping()

    cursor.execute("SELECT violations FROM classes WHERE user = (%s) and name = (%s)", (u, clss))
    violations = ast.literal_eval(cursor.fetchall()[0][0])
    violations.append(binary)
    violations = str(violations)

    cursor.execute("UPDATE classes SET violations = (%s) WHERE user = (%s) and name = (%s)", (violations, u, clss))


def video(clss, user):
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
            with open(frame, 'rb') as File:
                binary = File.read()

        db.ping()

        cursor.execute("SELECT violations FROM classes WHERE user = (%s) and name = (%s)", (u, clss))
        violations = ast.literal_eval(cursor.fetchall()[0][0])
        violations.append(binary)
        violations = str(violations)

        cursor.execute("UPDATE classes SET violations = (%s) WHERE username = (%s) and name = (%s)", (violations, u, clss))


def main():

    #mode = "image"  # video/image
    # mode = "video"  # video/image
    # mode = "test"

    mode = input('what mode: ')
    clss = input('what class: ') # 回复 : 10C
    user = input('username: ') #  回复 : 1

    if mode == "image":
        dir = "images/5_0.jpg"
        im = cv2.imread(dir)
        image(im, clss, user, dir)
        cv2.waitKey(0)

    elif mode == "video":
        video(clss, user)

main()
