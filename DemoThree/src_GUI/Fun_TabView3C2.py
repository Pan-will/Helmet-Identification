import cv2
import threading
from PyQt5.QtCore import QFile,QEvent, QTimer, Qt
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
from PIL import ImageDraw,ImageFont,Image
from timeit import default_timer as timer
import math


from PyQt5.QtWidgets import QLabel

class Label(QLabel):
    def __init__(self):
        super(Label, self).__init__()
        self.state = 'z'
    def get_key(self):
        return self.state
    def keyPressEvent(self, QKeyEvent):  # 键盘某个键被按下时调用
        #参数1  控件
        if QKeyEvent.key()== Qt.Key_A:  #判断是否按下了A键
            #key()  是普通键
            self.state = 'a'
            print('按下了A键')
        if QKeyEvent.key()== Qt.Key_D:  #判断是否按下了键B
            #key()  是普通键
            self.state = 'd'
            print('按下了B键')
        if QKeyEvent.key()== Qt.Key_Space:  #判断是否按下了空格键
            #key()  是普通键
            self.state = 'k'
            print('按下了空格键')
        if QKeyEvent.key()== Qt.Key_W:  #判断是否按下了w键
            #key()  是普通键
            self.state = 'w'
            print('按下了w键')
        if QKeyEvent.key()== Qt.Key_S:  #判断是否按下了s键
            #key()  是普通键
            self.state = 's'
            print('按下了s键')

class C_DisPlay_Tab3:
    def __init__(self, ui, mainWnd,yolo):
        self.ui = ui
        self.mainWnd = mainWnd
        self.yolo = yolo

        self.mainWnd.label = Label()
        self.mainWnd.label.move(100, 100)
        # self.mainWnd.label.grabKeyboard()  # 控件开始捕获键盘
        # self.tabView = 3
        # 默认视频源为相机
        self.isCamera = False

        self.frameRate = 0
        self.currImg = ''

        # 信号槽设置
        # ui.bt_test3.clicked.connect(self.Open_Test)
        ui.bt_C3_Open.clicked.connect(self.Open_Test)
        ui.bt_C3_Close.clicked.connect(self.Close)

        # self.ui.bt_C2_Work.setEnabled(True)
        self.ui.bt_C3_Close.setEnabled(False)

        # 创建一个关闭事件并设为未触发
        self.stopEvent = threading.Event()
        self.stopEvent.clear()


    def Open_Test(self):    # 正常识别，识别违规时，不做数据库操作，只做安全帽佩戴演示，不记录入数据库
        if not self.isCamera:
            self.mainWnd.label.grabKeyboard()  # 控件开始捕获键盘
            self.fileName, self.fileType = QFileDialog.getOpenFileName(self.mainWnd, 'Choose file', '', '*.mp4')
            self.cap = cv2.VideoCapture(self.fileName)
            self.frameRate = self.cap.get(cv2.CAP_PROP_FPS)#读取视频的fps
            self.total = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))#获取总时长
        else:
            # 下面两种rtsp格式都是支持的
            # cap = cv2.VideoCapture("rtsp://admin:Supcon1304@172.20.1.126/main/Channels/1")
            self.cap = cv2.VideoCapture(0)

            # 创建视频显示线程
        th = threading.Thread(target=self.Display)
        th.start()


    def Close(self):
        # 关闭事件设为触发，关闭视频播放
        self.ui.bt_C3_Open.setEnabled(True)
        self.ui.bt_C3_Close.setEnabled(False)
        self.ui.lb_video3.setText('请先打开要检测的本地视频')
        self.mainWnd.label.releaseKeyboard()  # 停止捕获键盘
        # self.ui.lb_C3_state.clear()
        self.stopEvent.set()


    def Display(self):
        self.ui.bt_C3_Open.setEnabled(False)
        self.ui.bt_C3_Close.setEnabled(True)

        # face = face_rec()
        start = timer()
        t = 0
        FPS = 0
        curr_num_frame = 1 # 记录当前第几帧
        timeF = 1  # 每隔timeF帧
        speed = 1# 当前倍速
        while self.cap.isOpened():

            if  timeF != 1:
                curr_num_frame += timeF
                if curr_num_frame >= self.total:
                    self.Close()
                    break
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, curr_num_frame)
                # continue
            success, frame = self.cap.read()
            # face.recognize(frame)
            # RGB转BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = Image.fromarray(frame)
            frame,details = self.yolo.detect_image(frame)  # 转成Image格式

            height,width = frame.size

            r = 790.0 / width
            dim = (780,int(height*r))
            frame.thumbnail(dim)#对图片进行缩放
            fontpath = "font/simsun.ttc"
            font = ImageFont.truetype(fontpath, 32)

            draw = ImageDraw.Draw(frame)
            # 绘制文字信息

            if curr_num_frame >= self.total:#大于总时长，则结束
                self.Close()
                break

            # waitKey = cv2.waitKey(1)
            waitKey = self.mainWnd.label.get_key()

            # print('haha:')
            if waitKey == 'k':#按空格进行暂停/继续
                cv2.waitKey(0)

            if waitKey == 'a':#按a进行快退十秒
                curr_num_frame = curr_num_frame - 10*self.frameRate
                if curr_num_frame < 0:
                    curr_num_frame = 1
                frameToStart = curr_num_frame

                self.cap.set(cv2.CAP_PROP_POS_FRAMES, frameToStart)
            if waitKey == 'd':  # 按d进行快进十秒
                curr_num_frame = curr_num_frame + 10 * self.frameRate
                if curr_num_frame >= self.total:#大于总时长，则结束
                    self.Close()
                else:
                    frameToStart = curr_num_frame
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, frameToStart)
            if waitKey == 's':  # 按's'进行倍速减
                speed = (speed / 2) if speed > 1 else 1 #最小倍速为1倍
                if speed > 1:
                    timeF = speed * self.frameRate
                if speed == 1:
                    timeF = 1
            if waitKey == 'w':  # 按'w'进行倍速增
                speed = (speed * 2) if speed * 2 < 16 else 8    #最大倍速为8倍
                if speed > 1:
                    timeF = speed * self.frameRate
                if speed == 1:
                    timeF = 1
            # print('waitKey值为：',waitKey)
            if waitKey != 'k':
                self.mainWnd.label.state = 'z'

            state_seconds = curr_num_frame/self.frameRate # 目前第几秒数据
            m, s = divmod(state_seconds, 60)
            h, m = divmod(m, 60)
            str_time = str("%d:%02d:%02d" % (h, m, s))
            # str_time = str(int(state_seconds//60//60)) + ':' +str(int(state_seconds//60)) + ':' + str(int(state_seconds%60))
            state_speed = '倍速：'+str(speed)
            if speed == 1:# 倍速若为1，即为正常播放，则不提示倍速信息
                state_speed=''
            # self.ui.lb_C3_state.setText('状态：'+str_time + '  ' + state_speed)
            state_Text = str_time + '  ' + state_speed

            if FPS >= 15:
                draw.text((int(math.fabs((frame.width-790)/2)+10), int(math.fabs((frame.height-445)/2)+10)), "FPS："+str(FPS) + '   ' + state_Text, font=font, fill=(0, 255, 0))
            else:
                draw.text((int(math.fabs((frame.width-790)/2)+10), int(math.fabs((frame.height-445)/2)+10)), "FPS：" + str(FPS) + '   ' + state_Text, font=font, fill=(255, 0, 0))
            bk_img = np.asarray(frame)  # bk_img是np格式的图片
            img = QImage(bk_img.data, bk_img.shape[1], bk_img.shape[0], QImage.Format_RGB888)


            self.ui.lb_video3.setPixmap(QPixmap.fromImage(img))#将帧数画面显示



            # if self.isCamera:
            #     cv2.waitKey(1)
            # else:
            #     delayTime = int(1000 / self.frameRate) - 20
            #     cv2.waitKey(delayTime)
                # # cv2.waitKey(int(self.frameRate))
                # cv2.waitKey(40)

            end = timer()
            if end - start >= 1:
                start = timer()
                FPS = t
                t = 0
            t += 1
            curr_num_frame += 1
            # 判断关闭事件是否已触发
            if True == self.stopEvent.is_set():
                # 关闭事件置为未触发，清空显示label
                self.stopEvent.clear()
                self.ui.lb_video3.clear()
                # self.ui.lb_C3_state.clear()
                # self.ui.bt_C2_Test.setEnabled(False)
                self.cap.release()
                self.mainWnd.label.releaseKeyboard()  # 停止捕获键盘
                break

    # def Enroll(self):
    #     self.ui.bt_C1_Open.setEnabled(True)
    #     self.ui.bt_C1_Enroll.setEnabled(False)

        # 对数据库添加数据，并提示签到成功

        # self.ui.lb_C1_Reminder.setText('签到成功')
        # pass