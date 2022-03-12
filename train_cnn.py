import identify
import attitude
import CNN

import os
import numpy as np
import cv2


cnn = CNN.CNN_Attitude()
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
    images_path = allFileFromDir("train_image/")
    images_path = allFileFromDir("images/")

    images_list = []
    label_list = []

    print(images_path)
    # 遍历每个图片
    for image_path in images_path:
        # 从名字中读取是否为违规图片, 如果是1，那就是有违规，如果是0，没有违规
        label = get_b_violation_in_name(image_path)
        label = int(label)
        if label != 1 and label != 0:
            label_list.append(0)
        else:
            label_list.append(label)

    i = 0
    for image_path in images_path:
        # 将图片中人物分割出来，然后传入姿态检测，获得到每个人物身上的特征点，组成列表，结合stable传入cnn训练
        image = cv2.imread(image_path)

        image_path_list, original_image, b_have_people = capture.get_people_location(image)

        if not b_have_people:
            print("not people")
        else:
            # 读取图片
            im = original_image
            # （1440*1080）
            # print(np.shape(im))
            frame = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            # print(np.shape(frame))
            images_list.append(frame)

        net_input = images_list[i]
        net_input = cv2.resize(net_input, (500, 281))
        net_input = [net_input]
        print(image_path + "中，有：" + str(len(image_path_list)) + "个人：")
        print("该图片是否违规：" + str(label_list[i]))

        # 如果图片的形状不对，无法训练
        if np.shape(net_input) != (1, 281, 500, 3):
            print("图片尺寸不对，无法训练...   该图片尺寸为：" + str(np.shape(net_input)) + " 需要的尺寸是(1, 281, 500, 3)")
        else:
            print("正在训练...")
            if label_list[i] == 0:
                train_label = [[1, 0]]
            else:
                train_label = [[0, 1]]
            loss = cnn.train(input_=net_input, label=train_label)
            print("损失为：" + str(loss))
        i += 1

    cnn.save()


train()