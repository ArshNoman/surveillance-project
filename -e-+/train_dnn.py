import identify
import attitude
import DNN

import os
import numpy as np
import cv2
import tensorflow as tf


dnn = DNN.DNN_Attitude()
attitude_net = attitude.attitude()
capture = identify.capture()

def allFileFromDir(Dirpath):
    """获取文件夹中所有文件的路径"""
    pathDir = os.listdir(Dirpath)
    pathfile = []
    for allDir in pathDir:
        child = os.path.join('%s%s' % (Dirpath, allDir))
        pathfile.append(child)
    return pathfile

# 从名字中获得是否违规
def get_b_violation_in_name(name_str=""):

    name_str = name_str.split("_", 1)
    label = name_str[1].split(".", 1)
    label = label[0]

    return label

def train():
    # 读取路径下的所有文件的路径
    images_path = allFileFromDir("images/")

    images_list = []
    label_list = []

    print(images_path)
    # 遍历每个图片
    for image_path in images_path:
        # 从名字中读取是否为违规图片, 如果是1，那就是有违规，如果是0，没有违规
        label = get_b_violation_in_name(image_path)
        label = int(label)
        # print(label)

        if label != 1 and label != 0:
            label_list.append(0)
        else:
            label_list.append(label)
    print(label_list)

    i = 0
    for image_path in images_path:
        people_points_list = np.zeros([18])
        # 将图片中人物分割出来，然后传入姿态检测，获得到每个人物身上的特征点，组成列表，结合stable传入cnn训练
        image = cv2.imread(image_path)
        # print(np.shape(image))
        temp_paths_list, original_image, b_have_people = capture.get_people_location(image)
        images_list = []
        if not b_have_people:
            print("not people")
        else:
            for path in temp_paths_list:
                # 读取图片
                im = cv2.imread(path)
                # （1440*1080）
                frame = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                images_list.append(frame)

            people_points_list = attitude_net.get_all_people_point_list(images_list)
        input_net = []  # 最大容量为10个人，36 * 10的点参数
        temp_ = 0
        for point_list in people_points_list:
            if temp_ < 10:
                for j in point_list:
                    input_net.append(j)
            temp_ += 1
        if len(input_net) < 36 * 10:
            for j in range((36 * 10) - len(input_net)):
                input_net.append(0)
        print(image_path + "中，有：" + str(len(people_points_list)) + "个人：")
        print(input_net)
        print("该图片是否违规：" + str(label_list[i]))
        print("正在训练...")
        input_net = [input_net]
        # input_net = tf.reshape(input_net, [-1, 36, 10])
        if label_list[i] == 0:
            train_label = [[1, 0]]
        else:
            train_label = [[0, 1]]
        loss = dnn.train(input_=input_net, label=train_label)
        print("损失为：" + str(loss))
        i += 1

    dnn.save()


train()