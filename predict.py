import DNN
import CNN
import attitude
import identify
import cv2
import numpy as np

capture = identify.capture()
attitude_net = attitude.attitude()
cnn = CNN.CNN_Attitude()
dnn = DNN.DNN_Attitude()

def predict_cnn(image):

    image_path_list, original_image, b_have_people = capture.get_people_location(image=image)

    is_violation = False

    if not b_have_people:
        return is_violation
    else:
        # 读取图片
        im = original_image
        # （1440*1080）
        # print(np.shape(im))
        frame = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (500, 281))

    net_input = [frame]

    # 如果图片的形状不对，无法预测
    if np.shape(net_input) != (1, 281, 500, 3):
        print("尺寸不对，无法预测...   该图片尺寸为：" + str(np.shape(net_input)) + " 需要的尺寸是(1, 281, 500, 3)")
    else:
        is_violation = cnn.predict(net_input)

    return is_violation

def predict_dnn(image):
    image_path_list, original_image, b_have_people = capture.get_people_location(image=image)
    frame = []
    images_list = []
    people_points_list = []
    is_violation = False

    if not b_have_people:
        return is_violation
    else:
        for path in image_path_list:
            # 读取图片
            im = cv2.imread(path)
            # （1440*1080）
            frame = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            images_list.append(frame)

        people_points_list = attitude_net.get_all_people_point_list(images_list)
        net_input = []  # 最大容量为10个人，36 * 10的点参数
        temp_ = 0
        for point_list in people_points_list:
            if temp_ < 10:
                for j in point_list:
                    net_input.append(j)
            temp_ += 1
        if len(net_input) < 36 * 10:
            for j in range((36 * 10) - len(net_input)):
                net_input.append(0)

        net_input = [net_input]
        is_violation = dnn.predict(net_input)

        return is_violation



    pass


