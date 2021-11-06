import cv2
import threading
from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
import numpy as np
from PIL import ImageDraw,ImageFont,Image
from timeit import default_timer as timer
import math
import copy
import datetime


class C_DisPlay_Tab2:
    def __init__(self, ui, mainWnd,yolo,face_rec):
        self.ui = ui
        self.mainWnd = mainWnd
        self.yolo = yolo
        self.face_rec = face_rec
        self.allLabels = self.getAllLabels()
        self.list_C2_DBInfo = ui.list_C2_DBInfo

        self.tabView = 2
        # 默认视频源为相机
        self.isCamera = True
        self.pattern = 0 # 0是测试模式，1是工作模式

        self.frameRate = 0
        self.currImg = ''

        # 信号槽设置
        ui.bt_C2_Test.clicked.connect(self.Open_Test)
        ui.bt_C2_Work.clicked.connect(self.Open_Work)
        ui.bt_C2_Close.clicked.connect(self.Close)

        # self.ui.bt_C2_Work.setEnabled(True)
        self.ui.bt_C2_Close.setEnabled(False)

        # 创建一个关闭事件并设为未触发
        self.stopEvent = threading.Event()
        self.stopEvent.clear()


    def Open_Test(self):    # 正常识别，识别违规时，不做数据库操作，只做安全帽佩戴演示，不记录入数据库
        if not self.isCamera:
            self.fileName, self.fileType = QFileDialog.getOpenFileName(self.mainWnd, 'Choose file', '', '*.mp4')
            self.cap = cv2.VideoCapture(self.fileName)
            self.frameRate = self.cap.get(cv2.CAP_PROP_FPS)
        else:
            # 下面两种rtsp格式都是支持的
            # cap = cv2.VideoCapture("rtsp://admin:Supcon1304@172.20.1.126/main/Channels/1")
            self.cap = cv2.VideoCapture(0)

            # 创建视频显示线程
        self.pattern = 0 # 状态置为测试模式
        th = threading.Thread(target=self.Display)
        th.start()

    def Open_Work(self):    # 正常识别，识别违规时，记录入数据库
        if not self.isCamera:
            self.fileName, self.fileType = QFileDialog.getOpenFileName(self.mainWnd, 'Choose file', '', '*.mp4')
            self.cap = cv2.VideoCapture(self.fileName)
            self.frameRate = self.cap.get(cv2.CAP_PROP_FPS)
        else:
            # 下面两种rtsp格式都是支持的
            # cap = cv2.VideoCapture("rtsp://admin:Supcon1304@172.20.1.126/main/Channels/1")
            self.cap = cv2.VideoCapture(0)

            # 创建视频显示线程
        self.pattern = 1 # 状态置为工作模式
        th = threading.Thread(target=self.Display)
        th.start()

    def Close(self):
        # 关闭事件设为触发，关闭视频播放
        self.ui.bt_C2_Test.setEnabled(True)
        self.ui.bt_C2_Work.setEnabled(True)
        self.ui.bt_C2_Close.setEnabled(False)

        self.stopEvent.set()


    def Display(self):
        self.ui.bt_C2_Test.setEnabled(False)
        self.ui.bt_C2_Work.setEnabled(False)
        self.ui.bt_C2_Close.setEnabled(True)

        # face = face_rec()
        start = timer()
        t = 0
        FPS = 0

        while self.cap.isOpened():
            success, frame = self.cap.read()
            # face.recognize(frame)
            # RGB转BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            frame = Image.fromarray(frame)
            frame,details = self.yolo.detect_image(frame)  # 转成Image格式
            # details格式如例：[{'label': 'hat', 'score': 0.9088244, 'left': 234, 'top': 82, 'right': 485, 'bottom': 413}]
            if self.pattern == 1:#若处在工作模式，则进行人脸的识别，数据库的交互
                for detail in details:
                    if detail['label'] == 'person':
                        self.currImg = copy.deepcopy(frame)#将缩放后的帧图暂存一份
                        self.after_face(self.currImg,detail)#之后对人脸进行判别
                pass
            height,width = frame.size
            # width = frame.width

            r = 790.0 / width
            dim = (790, int(height * r))
            frame.thumbnail(dim)

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


            self.ui.lb_video2.setPixmap(QPixmap.fromImage(img))#将帧数画面显示

            if self.isCamera:
                cv2.waitKey(1)
            else:
                cv2.waitKey(int(1000 / self.frameRate))

            end = timer()
            if end - start >=1:
                start = timer()
                FPS = t
                t = 0
            t += 1

            # 判断关闭事件是否已触发
            if True == self.stopEvent.is_set():
                # 关闭事件置为未触发，清空显示label
                self.stopEvent.clear()
                self.ui.lb_video2.clear()
                self.ui.lb_video2.setText('请先开启摄像头')
                # self.ui.bt_C2_Test.setEnabled(False)
                self.cap.release()

                break

    def getAllLabels(self):
        str_sql = "select num from worker_info order by num ASC"

        query = QSqlQuery()
        query.prepare(str_sql)

        # 将查询到的数据放至items列表中
        items_num = []
        # items_name = []
        if not query.exec_():
            query.lastError()
        else:
            while query.next():
                num = query.value(0)
                # name = query.value(1)
                items_num.append(num)
                # items_name.append(name)
        # return [items_num,items_name]
        # print(items_num)
        return items_num

    def after_face(self,image,detail):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("./ext/db/mydb.db")
        self.db.open()
        # detail格式如例：{'label': 'hat', 'score': 0.9088244, 'left': 234, 'top': 82, 'right': 485, 'bottom': 413}
        face_img = image.crop(
            (detail['left'], detail['top'], detail['right'], detail['bottom'] + 15))  # 检测到的目标部分
        success, labelIndex, pro = self.face_rec.face_recogniton(face_img)
        if success:  # 检测成功,检测到了人脸
            rec_num = self.allLabels[labelIndex]  # 识别的职工号
            now_time = datetime.datetime.now().timetuple()  # 得到的是结构体，形如time.struct_time(tm_year=2017, tm_mon=3, tm_mday=24, tm_hour=19, tm_min=37, tm_sec=3, tm_wday=4, tm_yday=83, tm_isdst=-1)
            # print(now_time)
            # 获取年月日值
            time_YMD = str(now_time.tm_year) + '/' + str(now_time.tm_mon) + '/' + str(now_time.tm_mday)
            # 检查今日是否已有违规记录
            str_sql = "select *  from violation_info WHERE num==" + str(rec_num) + " and CAST(time AS VARCHAR ) LIKE " + "'" + time_YMD + "%'"
            # str_sql = "select *  from sign_info WHERE num==1001 and CAST(time AS VARCHAR ) LIKE '2020/3/3%'"
            print(str_sql)
            query = QSqlQuery()
            query.prepare(str_sql)
            item_list = []
            if not query.exec_():
                query.lastError()
                # print('SQL错误原因：',query.lastError())
            else:
                while query.next():
                    item_list.append('*')
                    break

            # 记录违规信息，
            if len(item_list) == 0:
                query = QSqlQuery()
                now_time = time_YMD + ' ' + str(now_time.tm_hour) + ':' + str(now_time.tm_min) + ':' + str(
                    now_time.tm_sec)
                # print(now_time)
                insert_sql = "insert into violation_info values ( NULL" + "," + str(rec_num) + ",\'" + now_time + "\')"
                print(insert_sql)
                query.prepare(insert_sql)
                if not query.exec_():
                    print('插入失败')
                    pass
                else:
                    print('插入违规信息成功！')
                    self.update_list_C2_DBInfo(time_YMD + '%') # '更新侧栏违规信息！'
            else:
                print('今日已记录过')
            # self.update_list_C2_DBInfo(time_YMD + '%')  # '更新侧栏违规信息！'

    def update_list_C2_DBInfo(self,time):# 对侧栏今日违规未戴安全帽信息进行实时更新
        str_sql = "select worker_info.num,worker_info.name,violation_info.time " \
                  "from violation_info,worker_info " \
                  "WHERE worker_info.num==violation_info.num and CAST(violation_info.time AS VARCHAR ) LIKE " + "'" + time + "'" + " ORDER BY violation_info.time DESC"
        query = QSqlQuery()
        query.prepare(str_sql)
        # print(str_sql)

        # 将查询到的数据放至item_list列表中
        item_list1 = []
        # item_list4 = []
        if not query.exec_():
            query.lastError()
        else:
            while query.next():
                id = query.value(0)
                name = query.value(1)
                time_data = query.value(2)
                item_list1.append(str(id) + '-' + str(name) + '\t' + str(time_data))
                # item_list4.append(str(id) + '\t' + str(name) + '\t' + str(time))

        self.list_C2_DBInfo.clear()  # 先将list_C2_DBInfo控件内容清空
        # 添加两个空白行
        self.list_C2_DBInfo.addItems([' '])
        self.list_C2_DBInfo.addItems([' '])
        self.list_C2_DBInfo.addItems(['****************************************'])

        if len(item_list1) == 0:  # 若数据库中无今日数据
            self.list_C2_DBInfo.addItems(['\t暂无数据'])
        else:  # 若数据库中有今日数据
            self.list_C2_DBInfo.addItems(['职员\t日期'])
            self.list_C2_DBInfo.addItems(item_list1)
