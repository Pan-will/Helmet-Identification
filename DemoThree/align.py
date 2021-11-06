import cv2
import numpy as np
from nets.nets_face.mtcnn import mtcnn
import utils.utils_face.utils as utils
from nets.nets_face.inception import InceptionResNetV1
import os



# 创建mtcnn对象
mtcnn_model = mtcnn()




def mtcnn_update_img(img,name):
    # 门限函数
    threshold = [0.5,0.7,0.9]
    # 检测人脸
    rectangles = mtcnn_model.detectFace(img, threshold)

    draw = img.copy()
    # 转化成正方形
    rectangles = utils.rect2square(np.array(rectangles))

    # 载入facenet
    facenet_model = InceptionResNetV1()
    # model.summary()
    model_path = './model_data/model_data_face/facenet_keras.h5'
    facenet_model.load_weights(model_path)


    for rectangle in rectangles:
        if rectangle is not None:
            landmark = (np.reshape(rectangle[5:15],(5,2)) - np.array([int(rectangle[0]),int(rectangle[1])]))/(rectangle[3]-rectangle[1])*160

            crop_img = img[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]

            # crop_img = cv2.resize(crop_img,(160,160))
            crop_img = cv2.resize(crop_img,(128,128))
            print("before：",name)
            cv2.imshow('调整水平前', crop_img)
            new_img,_ = utils.Alignment_1(crop_img,landmark)
            print("two eyes：",name)
            cv2.imshow('调整水平后',new_img)
            # cv2.imwrite(name, new_img)


def save_feces(img, name):
    cv2.imwrite(name, img)

RAW_IMAGE_DIR = 'face_dataset/dataset/new_aboil/'
DATASET_DIR = 'face_dataset/dataset/new_aboil/'
image_list = os.listdir(RAW_IMAGE_DIR)
count = 1
for image_path in image_list:
    image = cv2.imread(RAW_IMAGE_DIR + image_path)

    print(image_path)
    if count >= 0 :
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mtcnn_update_img(image,'%ss%d.jpg' % (DATASET_DIR, count))
    else:
        pass
    count += 1
    cv2.waitKey(1)