import numpy as np
import tensorflow.compat.v1 as tf
import os

# tf.disable_eager_execution()
# physical_devices = tf.config.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)

def softmax(x):
    probs = np.exp(x - np.max(x))
    probs /= np.sum(probs)
    return probs


class CNN_Attitude:
    def __init__(self):
        # Make a session
        self.session = tf.Session()
        self.width = tf.placeholder(tf.float32)
        self.height = tf.placeholder(tf.float32)
        self.input_states = tf.placeholder(tf.float32, shape=[None, 281, 500, 3])
        # 模型的真实值
        self.label = tf.placeholder(shape=[None, 2], dtype=tf.float32, name="label")

        self.conv1 = tf.layers.conv2d(inputs=self.input_states,
                                      filters=36, kernel_size=[3, 3],
                                      padding="same", data_format="channels_last",
                                      activation=tf.nn.relu)
        self.conv2 = tf.layers.conv2d(inputs=self.conv1, filters=54,
                                      kernel_size=[3, 3], padding="same",
                                      data_format="channels_last",
                                      activation=tf.nn.relu)
        self.conv3 = tf.layers.conv2d(inputs=self.conv2,
                                      filters=54, kernel_size=[3, 3],
                                      padding="same", data_format="channels_last",
                                      activation=tf.nn.relu)
        self.conv4 = tf.layers.conv2d(inputs=self.conv2,
                                      filters=1, kernel_size=[3, 3],
                                      padding="same", data_format="channels_last",
                                      activation=tf.nn.relu)

        # self.conv4 = tf.layers.dense(inputs=self.conv3, units=1000, activation=tf.nn.relu)

        self.conv_trans = tf.reshape(self.conv3, [-1, 281 * 500 * 3])

        # self.conv5 = tf.layers.dense(inputs=self.conv_trans, units=500, activation=tf.nn.relu)

        self.output = tf.layers.dense(inputs=self.conv_trans, units=2, activation=tf.nn.log_softmax)


        self.loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=self.output, labels=self.label))

        self.train_op = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss=self.loss)

        self.saver = tf.train.Saver()

        init = tf.global_variables_initializer()
        self.session.run(init)

        self.restore()

    def predict(self, net_input):
        is_violation = False
        probs = self.session.run([self.output], feed_dict={self.input_states: net_input})
        # output = np.argmax(probs)
        probs = probs[0][0]
        probs = softmax(probs)
        print(probs)
        if probs[0] > probs[1]:
            is_violation = False
        else:
            is_violation = True
        return is_violation

    def train(self, input_, label):

        loss = self.session.run([self.loss, self.train_op], feed_dict={self.input_states: input_, self.label: label})
        loss = loss[0]
        print("损失：", loss)
        return loss

    def save(self, save_path=""):
        if save_path == "":
            save_path = "saveModel_CNN/CNNModel.ckpt"

        self.saver.save(sess=self.session, save_path=save_path)

    # 模型恢复
    def restore(self, save_path=""):
        if save_path == "":
            save_path = "saveModel_CNN/CNNModel.ckpt"
        # 检查文件夹是否存在
        temp = os.path.exists(save_path)

        if temp:
            print("读取模型")
            # 模型恢复
            self.saver.restore(sess=self.session, save_path="saveModel/CNNModel.ckpt")
            pass
        else:
            print("不存在训练好的模型，无法恢复")
            pass




