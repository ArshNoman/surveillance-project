import cv2
import numpy as np

class attitude:
    def __init__(self):
        # 配置文件
        # protoFile = 'openpose-master\models\pose\coco\pose_deploy_linevec.prototxt'
        # weightsfile = 'openpose-master\models\pose\coco\pose_iter_440000.caffemodel'
        self.protoFile = 'Class/pose_deploy_linevec.prototxt'
        self.weightsfile = 'Class/pose_iter_440000.caffemodel'
        self.npoints = 18
        POSE_PAIRS = [[1, 0], [1, 2], [1, 5], [2, 3], [3, 4], [5, 6], [6, 7], [1, 8], [8, 9], [9, 10], [1, 11], [11, 12],
                      [12, 13], [0, 14], [0, 15], [14, 16], [15, 17]]
        self.net = cv2.dnn.readNetFromCaffe(self.protoFile, self.weightsfile)

    def detect_(self, img):

        # print(img.shape)
        inHeight = img.shape[0]  # 1440
        inWidth = img.shape[1]  # 1080
        netInputsize = (368, 368)
        # 将当前帧传入网络，获得人体各个点位的位置信息
        self.net = cv2.dnn.readNetFromCaffe(self.protoFile, self.weightsfile)
        inpBlob = cv2.dnn.blobFromImage(img, 1.0 / 255, netInputsize, (0, 0, 0), swapRB=True, crop=False)
        self.net.setInput(inpBlob)
        output = self.net.forward()

        scaleX = float(inWidth) / output.shape[3]
        scaleY = float(inHeight) / output.shape[2]
        points = []
        threshold = 0.1

        # 获得到点在图片中的位置
        for i in range(self.npoints):
            probMap = output[0, i, :, :]  # shape(46*46)
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
            x = scaleX * point[0]
            y = scaleY * point[1]
            if prob > threshold:
                points.append((int(x), int(y)))
            else:
                points.append(None)

        # 对数据进行编码为[36]的列表
        point_list = []
        for i, p in enumerate(points):
            x = y = 0
            if p is not None:
                x = p[0]
                y = p[1]

            point_list.append(x)
            point_list.append(y)

            # enumerate把points的值前面带上索引i
            cv2.circle(img, p, 4, (255, 255, 0), thickness=1, lineType=cv2.FILLED)
            # cv2.putText(img, '{}'.format(i), p, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, lineType=cv2.LINE_AA)
        # print("位置列表：")
        # print(point_list)
        # cv2.imshow("image", img)

        return point_list

    # 传入一列表的图片，获得里面的所有图片的特征点
    def get_all_people_point_list(self, img_list):

        points_list = []

        for img in img_list:
            point = self.detect_(img)
            points_list.append(point)
            # cv2.waitKey(0)

        # print(points_list)
        return points_list

    # 用于测试
    def test(self, image):
        points_list = []
        point = self.detect_(image)
        points_list.append(point)
