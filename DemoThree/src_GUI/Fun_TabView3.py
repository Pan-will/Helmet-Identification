import cv2
import threading
from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
from PIL import ImageDraw,ImageFont,Image
from timeit import default_timer as timer
import math


class C_DisPlay_Tab3:
    def __init__(self, ui, mainWnd,yolo):
        self.ui = ui
        self.mainWnd = mainWnd
        self.yolo = yolo
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
            success, frame = self.cap.read()
            if (curr_num_frame % timeF != 0):
                continue
            # face.recognize(frame)
            # RGB转BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame,details = self.yolo.detect_image(Image.fromarray(frame))  # 转成Image格式
            frame = Image.fromarray(frame)
            height,width = frame.size

            r = 790.0 / width
            dim = (780,int(height*r))
            frame.thumbnail(dim)#对图片进行缩放
            fontpath = "font/simsun.ttc"
            font = ImageFont.truetype(fontpath, 32)

            draw = ImageDraw.Draw(frame)
            # 绘制文字信息
            if FPS >= 15:
                draw.text((int(math.fabs((frame.width-790)/2)+10), int(math.fabs((frame.height-445)/2)+10)), "FPS："+str(FPS), font=font, fill=(0, 255, 0))
            else:
                draw.text((int(math.fabs((frame.width-790)/2)+10), int(math.fabs((frame.height-445)/2)+10)), "FPS：" + str(FPS), font=font, fill=(255, 0, 0))
            bk_img = np.asarray(frame)  # bk_img是np格式的图片
            img = QImage(bk_img.data, bk_img.shape[1], bk_img.shape[0], QImage.Format_RGB888)


            self.ui.lb_video3.setPixmap(QPixmap.fromImage(img))#将帧数画面显示

            if curr_num_frame >= self.total:#大于总时长，则结束
                self.Close()

            waitKey = cv2.waitKey(1)
            if waitKey & 0xff == ord(' '):#按空格进行暂停/继续
                cv2.waitKey(0)
            if waitKey & 0xff == ord('a'):#按a进行快退十秒
                curr_num_frame = curr_num_frame - 10*self.frameRate
                frameToStart = curr_num_frame if curr_num_frame>0 else 1
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, frameToStart)
            if waitKey & 0xff == ord('a'):  # 按d进行快进十秒
                curr_num_frame = curr_num_frame + 10 * self.frameRate
                if curr_num_frame >= self.total:#大于总时长，则结束
                    self.Close()
                else:
                    frameToStart = curr_num_frame
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, frameToStart)
            if waitKey & 0xff == 37:  # 按'<-'进行倍速减
                speed = (speed / 2) if speed > 1 else 1 #最小倍速为1倍
                timeF = speed * self.frameRate
            if waitKey & 0xff == 39:  # 按'->'进行倍速增
                speed = (speed * 2) if speed < 16 else 8    #最大倍速为8倍
                timeF = speed * self.frameRate

            state_seconds = curr_num_frame/self.frameRate # 目前第几秒数据
            m, s = divmod(state_seconds, 60)
            h, m = divmod(m, 60)
            str_time = str("%d:%02d:%02d" % (h, m, s))
            # str_time = str(int(state_seconds//60//60)) + ':' +str(int(state_seconds//60)) + ':' + str(int(state_seconds%60))
            state_speed = '倍速：'+str(speed)
            if speed == 1:# 倍速若为1，即为正常播放，则不提示倍速信息
                state_speed=''
            self.ui.lb_C3_state.setText('状态：'+str_time + state_speed)
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
                self.ui.lb_C3_state.clear()
                # self.ui.bt_C2_Test.setEnabled(False)
                self.cap.release()
                break

    # def Enroll(self):
    #     self.ui.bt_C1_Open.setEnabled(True)
    #     self.ui.bt_C1_Enroll.setEnabled(False)

        # 对数据库添加数据，并提示签到成功

        # self.ui.lb_C1_Reminder.setText('签到成功')
        # pass