"""-----------------------------------------
step 4:
    识别照片中的人脸；
-----------------------------------------"""
# -*-coding:utf8-*-
import sys
import cv2
from face_rec.load_dataset import read_name_list
from face_rec.train_model import Model
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
from PIL import Image
import numpy

import tensorflow as tf
from tensorflow.python.keras.backend import set_session
# 程序开始时声明
sess = tf.Session()
graph = tf.get_default_graph()

# 在model加载前添加set_session
set_session(sess)
# global graph
# global sess
import tensorflow as tf
graph = tf.get_default_graph()

class Face_Rec():
    def __init__(self):
        # self.allLabels = self.get_labels()# 获取员工职工号列表，即职工号列表
        self.face_engine = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt.xml')
        self.model = Model()
        self.model.load()


    def face_recogniton(self,image):

        image = cv2.cvtColor(numpy.asarray(image), cv2.COLOR_RGB2BGR)#将Image格式图片转为cv格式

        # 图片灰度化
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # print(gray)
        # 检测人脸，探测图片中的人脸
        faces = self.face_engine.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        if len(faces)>0:
            x, y, w, h = faces[0]
            origin = gray[x:x + w, y:y + h]
            origin = cv2.resize(origin, (128, 128), interpolation=cv2.INTER_LINEAR)
            with graph.as_default():
                set_session(sess)
                labelIndex, prob = self.model.predict(origin)
            # 如果模型认为概率高于70%则显示为模型中已有的label
            # print('self.allLabels',allLabels)
            if prob > 0.7:
                # predict_label = allLabels[labelIndex]
                # print(predict_label, prob)
                return True,labelIndex,prob
            else:
                labelIndex = 'unknown'
                print("Don't know this person.")
                return False, labelIndex, 0

        else:
            labelIndex = '*'#未检测到人脸
            print("未检测到人脸！")
            return False, labelIndex, 0

#
# faces = Face_Rec()
# # 待测试图片路径
# path = 'D:\\workspaces\\qt5\\hat_recognition\\demo2\\img\\s1.jpg'
# # 读取图片
# image = cv2.imread(path)
# cv2.imshow('image', image)
# # cv2.waitKey(3000)
# success,predict_label,pro = faces.face_recogniton(image,[1001,1002])
