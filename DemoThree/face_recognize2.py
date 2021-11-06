import cv2
import os
import numpy as np
from nets.nets_face.mtcnn import mtcnn
import utils.utils_face.utils as utils
from nets.nets_face.inception import InceptionResNetV1
from timeit import default_timer as timer

class face_rec():
    def __init__(self):
        # 创建mtcnn对象
        # 检测图片中的人脸
        self.mtcnn_model = mtcnn()
        # 门限函数
        self.threshold = [0.5, 0.8, 0.9]

        # 载入facenet
        # 将检测到的人脸转化为128维的向量
        self.facenet_model = InceptionResNetV1()
        # model.summary()
        model_path = './model_data/model_data_face/facenet_keras.h5'
        self.facenet_model.load_weights(model_path)

        # -----------------------------------------------#
        #   对数据库中的人脸进行编码
        #   known_face_encodings中存储的是编码后的人脸
        #   known_face_names为人脸的名字
        # -----------------------------------------------#
        face_list = os.listdir("facesnet_dataset")

        self.known_face_encodings = []

        self.known_face_names = []

        for face in face_list:

            name = face.split(".")[0]

            img = cv2.imread("./facesnet_dataset/" + face)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            #
            # # 检测人脸
            rectangles = self.mtcnn_model.detectFace(img, self.threshold)
            #
            if rectangles == []:
                # self.known_face_encodings.append([])
                # self.known_face_names.append('name')
                continue
            # 转化成正方形
            rectangles = utils.rect2square(np.array(rectangles))
            # facenet要传入一个160x160的图片
            rectangle = rectangles[0]
            # 记下他们的landmark
            landmark = (np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])) / (
            rectangle[3] - rectangle[1]) * 160

            crop_img = img[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
            # print('图片：',name)
            try:
                crop_img = cv2.resize(crop_img, (160, 160))
                print('图片：', name, 'rectangle：', rectangles)
            except:
                # self.known_face_encodings.append([])
                # self.known_face_names.append('name')
                continue
            new_img, _ = utils.Alignment_1(crop_img, landmark)
            #
            new_img = np.expand_dims(new_img, 0)
            # 将检测到的人脸传入到facenet的模型中，实现128维特征向量的提取
            face_encoding = utils.calc_128_vec(self.facenet_model, new_img)
            print(type(face_encoding))
            self.known_face_encodings.append(face_encoding)
            print(self.known_face_encodings)
            self.known_face_names.append(name)

    def recognize(self, draw):
        # -----------------------------------------------#
        #   人脸识别
        #   先定位，再进行数据库匹配
        # -----------------------------------------------#
        height, width, _ = np.shape(draw)
        draw_rgb = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

        # 检测人脸
        rectangles = self.mtcnn_model.detectFace(draw_rgb, self.threshold)

        if len(rectangles) == 0:
            return

        # 转化成正方形
        rectangles = utils.rect2square(np.array(rectangles, dtype=np.int32))
        rectangles[:, 0] = np.clip(rectangles[:, 0], 0, width)
        rectangles[:, 1] = np.clip(rectangles[:, 1], 0, height)
        rectangles[:, 2] = np.clip(rectangles[:, 2], 0, width)
        rectangles[:, 3] = np.clip(rectangles[:, 3], 0, height)
        # -----------------------------------------------#
        #   对检测到的人脸进行编码
        # -----------------------------------------------#
        face_encodings = []
        for rectangle in rectangles:
            landmark = (np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])) / (
            rectangle[3] - rectangle[1]) * 160

            crop_img = draw_rgb[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
            crop_img = cv2.resize(crop_img, (160, 160))

            new_img, _ = utils.Alignment_1(crop_img, landmark)
            new_img = np.expand_dims(new_img, 0)

            face_encoding = utils.calc_128_vec(self.facenet_model, new_img)
            face_encodings.append(face_encoding)

        face_names = []
        for face_encoding in face_encodings:
            # 取出一张脸并与数据库中所有的人脸进行对比，计算得分
            matches = utils.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.9)
            name = "Unknown"
            # 找出距离最近的人脸
            face_distances = utils.face_distance(self.known_face_encodings, face_encoding)
            # 取出这个最近人脸的评分
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        rectangles = rectangles[:, 0:4]
        # -----------------------------------------------#
        #   画框~!~
        # -----------------------------------------------#
        for (left, top, right, bottom), name in zip(rectangles, face_names):
            cv2.rectangle(draw, (left, top), (right, bottom), (0, 0, 255), 2)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(draw, name, (left, bottom - 15), font, 0.75, (255, 255, 255), 2)
        return draw


if __name__ == "__main__":

    dududu = face_rec()
    video_path = 'C:\\Users\\Aboil\Desktop\\video_testFile\\20200108_193929.mp4'
    video_capture = cv2.VideoCapture(video_path)
    start = 0

    # 读取视频时长（帧总数）
    total = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print("[INFO] {} total frames in video".format(total))

    # 设定从视频的第几帧开始读取
    # From :  https://blog.csdn.net/luqinwei/article/details/87973472
    frameToStart = 1
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, frameToStart)

    while True:
        start_time = timer()
        ret, draw = video_capture.read()
        if start >1:
            height = draw.shape[0]
            width = draw.shape[1]

            r = 790.0 / width
            dim = (780, int(height * r))
            frame = cv2.resize(draw, dim, interpolation=cv2.INTER_NEAREST)
            dududu.recognize(frame)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1):
                if 0xFF == ord('q'):
                    break
                elif 0xFF == ord('a'):
                    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 200)
        start += 1
        print('每帧耗时：', timer()-start_time)
    video_capture.release()
    cv2.destroyAllWindows()