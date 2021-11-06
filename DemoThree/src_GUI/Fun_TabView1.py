import sys
import os
from PIL import Image
import cv2
import threading
from PyQt5.QtCore import QFile
from PyQt5.QtWidgets import QFileDialog, QMessageBox,QDesktopWidget,QApplication, QMainWindow
from PyQt5.QtGui import QImage, QPixmap
import numpy as np
from PIL import ImageDraw,ImageFont,Image
from src_GUI.UI_Dialog_AddStaff import Ui_Dialog
from src_GUI.UI_Dialog_UpdateData import Ui_Dialog_Update
from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
import numpy
import copy
import datetime
import shutil

def center(mainWnd):
    # 获取屏幕的长宽
    screen = QDesktopWidget().screenGeometry()
    # 使主窗口居中
    mainWnd.move((screen.width() - 1100) / 2, (screen.height() - 649) / 2 - 20)


class get_dialogUI_addStaff(QtWidgets.QWidget,Ui_Dialog):
    def __init__(self):
        super(get_dialogUI_addStaff,self).__init__()
        self.setupUi(self)
        self.bt_C12_ChooseImg.clicked.connect(self.Get_Img)
        self.bt_C12_Cancel.clicked.connect(self.Close)
        self.bt_C12_Submit.clicked.connect(self.Submit)
        self.fileName = ''

    def Get_Img(self):
        # self.fileName保存的是选择的图片路径
        self.fileName, self.fileType = QFileDialog.getOpenFileName(self, '选择图片文件', '', '*.jpg;;*.png;;*.jpeg;;*.bmp')   # 最后一个参数是指定文件类型
        print(self.fileName)
        img = Image.open(self.fileName).convert("RGB")
        # image.show()

        height,width = img.size

        r = 250.0 / width
        dim = (240, int(height * r))
        img.thumbnail(dim)  # 对图片进行缩放
        bk_img = np.asarray(img)  # bk_img是np格式的图片
        img = QImage(bk_img.data, bk_img.shape[1], bk_img.shape[0], QImage.Format_RGB888)
        self.lb_C12_CurrImg.setPixmap(QPixmap.fromImage(img))  # 将帧数画面显示

    def Submit(self):
        # self.fileName, self.fileType = QFileDialog.getOpenFileName(self.mainWnd, 'Choose file', '', '*.jpg')
        # print(self.fileName, self.fileType)
        if self.input_C12_Num.text() == '' or self.input_C12_Name.text() == '':
            self.fileName = ''
            self.lb_C12_CurrImg.setText('请输入完整信息！')
            return
        elif self.fileName == '' :
            self.lb_C12_CurrImg.setText('请选择图片文件！')
            return
        else:
            # 对职工信息表进行查询，若该职工号已存在，则添加失败，并进行提示
            str_sql = "select * from worker_info WHERE worker_info.num==" + self.input_C12_Num.text()
            query = QSqlQuery()
            query.prepare(str_sql)
            item_list = []

            if not query.exec_():
                query.lastError()
            else:
                while query.next():
                    item_list.append('*')
            if len(item_list)!=0:
                self.fileName = ''
                self.lb_C12_CurrImg.setText('该职工号已存在！')
                return
            else:
                self.Add_Success()

    def Close(self):
        self.fileName = ''
        self.hide()

    def Add_Success(self):
        num = self.input_C12_Num.text()

        query = QSqlQuery()
        insert_sql = "insert into worker_info values (" + num + ",\'" + self.input_C12_Name.text() + "\',\'" + num + '.jpg\')'
        print(insert_sql)
        query.prepare(insert_sql)
        if not query.exec_():
            self.lb_C12_CurrImg.setText('添加失败！')
            self.fileName = ''#将图片重新置为空
            return
        img = Image.open(self.fileName)
        img.save('face_dataset/' + num + '.jpg')
        self.lb_C12_CurrImg.setText('添加成功！')


class get_dialogUI_update(QtWidgets.QWidget,Ui_Dialog_Update):
    def __init__(self):
        super(get_dialogUI_update,self).__init__()
        self.setupUi(self)
        self.bt_C12_ChooseH5.clicked.connect(self.Get_H5)
        self.bt_C12_ChooseDB.clicked.connect(self.Get_DB)
        self.bt_C12_Cancel.clicked.connect(self.Close)
        self.bt_C12_Submit.clicked.connect(self.Submit)
        self.fileName_H5 = ''
        self.fileName_DB = ''
        self.cwd = os.getcwd()#本项目所在目录，不是此文件所在目录

    def Get_H5(self):
        self.fileName_H5, self.fileType = QFileDialog.getOpenFileName(self, '选择图片文件', '', '*.h5')  # 最后一个参数是指定文件类型
        # 形如：self.fileName = 'D:/workspaces/model/model.h5'
        self.lb_C12_H5Name.setText('已选择：')
        if self.fileName_H5 != '':
            self.lb_C12_H5Name.setText('已选择：'+self.fileName_H5.split('/')[-1])
        print(self.cwd)

    def Get_DB(self):
        self.fileName_DB, self.fileType = QFileDialog.getOpenFileName(self, '选择图片文件', '', '*.db')  # 最后一个参数是指定文件类型
        # 形如：self.fileName = 'D:/workspaces/model/model.h5'
        self.lb_C12_DBName.setText('已选择：')
        if self.fileName_DB != '':
            self.lb_C12_DBName.setText('已选择：' + self.fileName_DB.split('/')[-1])

    def Close(self):
        self.hide()

    def Submit(self):
        if self.fileName_H5 != '':
            src_file = self.fileName_H5
            des_file = self.cwd + "\\face_rec\\face_rec_model\\" + "model.h5"
            shutil.copyfile(src_file, des_file)
            self.lb_C12_reminder.setText('操作成功！请务必重启系统以加载更换后的数据和模型！')

        if self.fileName_DB != '':
            src_file = self.fileName_DB
            des_file = self.cwd + "\\ext\\db\\" + "mydb.db"
            shutil.copyfile(src_file, des_file)
            self.lb_C12_reminder.setText('操作成功！请务必重启系统以加载更换后的数据和模型！')

        if self.fileName_H5 == '' and self.fileName_DB == '':
            self.lb_C12_reminder.setText('操作失败！请先选择文件！')



class C_DisPlay_Tab1:
    # def __init__(self, ui, mainWnd, hat_recognition):
    def __init__(self, ui, mainWnd,yolo,face_rec):
        center(mainWnd)#窗口居中
        self.ui = ui
        self.mainWnd = mainWnd
        self.yolo = yolo
        self.face_rec = face_rec
        self.allLabels = self.getAllLabels()
        # print(self.allLabels)
        # self.hat_model = hat_recognition
        self.tabView = 1
        self.list_C1_DBInfo = ui.list_C1_DBInfo
        # 默认视频源为相机
        self.isCamera = True

        self.currImg = ''
        self.rec_num = -1

        # 信号槽设置
        ui.bt_C1_Open.clicked.connect(self.Open)
        ui.bt_C1_PrintScreen.clicked.connect(self.PrintScreen)
        ui.bt_C1_Enroll.clicked.connect(self.Enroll)
        ui.bt_C1_Close.clicked.connect(self.Close)
        ui.bt_C1_Add.clicked.connect(self.Close)
        # ui.bt_C1_Add.clicked.connect(self.UI_AddStaff)
        ui.bt_C1_Add.clicked.connect(self.UI_Update)

        self.ui.bt_C1_PrintScreen.setEnabled(False)
        self.ui.bt_C1_Enroll.setEnabled(False)
        self.ui.bt_C1_Close.setEnabled(False)
        self.ui.bt_C1_Add.setEnabled(False)


        self.ui.lb_C1_Reminder.setText(' ')#设置提示文本的显示
        # 创建一个关闭事件并设为未触发
        self.stopEvent = threading.Event()
        self.stopEvent.clear()
    def getAllLabels(self):
        str_sql = "select num,name from worker_info order by num ASC"

        query = QSqlQuery()
        query.prepare(str_sql)

        # 将查询到的数据放至items列表中
        items_num = []
        items_name = []
        if not query.exec_():
            query.lastError()
        else:
            while query.next():
                num = query.value(0)
                name = query.value(1)
                items_num.append(num)
                items_name.append(name)
        return [items_num,items_name]
    def UI_AddStaff(self):
        # self.mainWnd.hide()
        self.mainWnd.dia = get_dialogUI_addStaff()
        self.mainWnd.dia.show()

    def UI_Update(self):
        # self.mainWnd.hide()
        self.mainWnd.dia_update = get_dialogUI_update()
        self.mainWnd.dia_update.show()


    def Open(self):
        self.ui.lb_C1_Reminder.setText(' ')#设置提示文本的显示
        if not self.isCamera:
            self.fileName, self.fileType = QFileDialog.getOpenFileName(self.mainWnd, 'Choose file', '', '*.mp4')
            self.cap = cv2.VideoCapture(self.fileName)
            self.frameRate = self.cap.get(cv2.CAP_PROP_FPS)
        else:
            # 下面两种rtsp格式都是支持的
            # cap = cv2.VideoCapture("rtsp://admin:Supcon1304@172.20.1.126/main/Channels/1")
            self.cap = cv2.VideoCapture(0)

            # 创建视频显示线程
        th = threading.Thread(target=self.Display)
        th.start()

    def PrintScreen(self):
        # 关闭事件设为触发，关闭视频播放
        self.ui.bt_C1_Enroll.setEnabled(True)
        self.ui.bt_C1_PrintScreen.setEnabled(False)
        self.ui.bt_C1_Close.setEnabled(True)

        self.stopEvent.set()

    def Close(self):
        # 关闭事件设为触发，关闭视频播放
        self.ui.bt_C1_Close.setEnabled(False)
        self.ui.bt_C1_Enroll.setEnabled(False)
        self.ui.bt_C1_PrintScreen.setEnabled(False)
        self.ui.bt_C1_Open.setEnabled(True)
        self.ui.lb_video1.clear()
        self.ui.lb_video1.setText('请先开启摄像头')
        self.ui.lb_C1_Reminder.setText(' ')  # 设置提示文本的显示
        # self.stopEvent.set()
        self.cap.release()

    def Display(self):
        self.ui.bt_C1_Open.setEnabled(False)
        self.ui.bt_C1_PrintScreen.setEnabled(True)
        self.ui.bt_C1_Close.setEnabled(True)
        self.ui.bt_C1_Add.setEnabled(True)

        # face = face_rec()
        while self.cap.isOpened():
            success, frame = self.cap.read()
            # face.recognize(frame)
            # RGB转BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            frame = Image.fromarray(frame)
            self.currImg = copy.deepcopy(frame)
            # frame = self.yolo.detect_image(frame)  # 转成Image格式

            height, width = frame.size
            # width = frame.width

            r = 790.0 / width
            dim = (790, int(height * r))
            frame.thumbnail(dim)
            # height = frame.shape[0]
            # width= frame.shape[1]
            # r = 790.0 / width
            # dim = (780,int(height*r))
            # frame = cv2.resize(frame, dim, interpolation=cv2.INTER_NEAREST)
            bk_img = np.asarray(frame)  # bk_img是np格式的图片
            img = QImage(bk_img.data, bk_img.shape[1], bk_img.shape[0], QImage.Format_RGB888)

            self.ui.lb_video1.setPixmap(QPixmap.fromImage(img))#将帧数画面显示

            if self.isCamera:
                cv2.waitKey(1)
            else:
                cv2.waitKey(int(1000 / self.frameRate))

            # 判断关闭事件是否已触发
            if True == self.stopEvent.is_set():
                # 关闭事件置为未触发，清空显示label
                self.stopEvent.clear()
                self.ui.lb_video1.clear()
                self.ui.bt_C1_Open.setEnabled(False)
                self.cap.release()
                fontpath = "font/simsun.ttc"
                font = ImageFont.truetype(fontpath, 32)
                # img_pil = Image.fromarray(self.currImg)
                img_pil = frame
                draw = ImageDraw.Draw(img_pil)
                # 绘制文字信息
                draw.text((width//2, height//2-50), "识别中……", font=font, fill=(0, 255, 0))
                bk_img = np.array(img_pil)  # bk_img是cv2格式的图片
                img = QImage(bk_img.data, bk_img.shape[1], bk_img.shape[0], QImage.Format_RGB888)
                self.ui.lb_video1.setPixmap(QPixmap.fromImage(img))  # 将帧数画面显示

                # 进行安全帽识别
                result_img,details = self.yolo.detect_image(self.currImg)  # details是列表，里面的元素是字典，
                # details格式如例：[{'label': 'hat', 'score': 0.9088244, 'left': 234, 'top': 82, 'right': 485, 'bottom': 413}][{'label': 'hat', 'score': 0.9088244, 'left': 234, 'top': 82, 'right': 485, 'bottom': 413}]
                str_result = ' '
                if len(details)==0:#未检测到目标
                    str_result = '未检测到目标，请重新拍摄！'
                else:
                    detail = details[0]
                    if detail['label'] == 'person':
                        str_result = '未佩戴安全帽，无法完成签到！请戴帽后重试！'
                    else:
                        face_img = self.currImg.crop((detail['left'],detail['top'],detail['right'],detail['bottom']+15))#检测到的目标部分
                        # face_img.show()
                        # self.currImg.show()
                        success, labelIndex, pro = self.face_rec.face_recogniton(face_img)
                        if success:#检测成功
                            # print(self.allLabels)
                            # print('预测结果索引：',labelIndex)
                            self.rec_num = self.allLabels[0][labelIndex]#识别的职工号
                            rec_name = self.allLabels[1][labelIndex]#识别的职工姓名
                            str_result = str(self.rec_num) + '-' + rec_name + ' 将进行签到……'
                        else:
                            if labelIndex =='unknown':#检测到了人脸，但未识别出是谁
                                str_result = '人脸识别失败！请重试……'
                            else:#未检测到人脸
                                str_result = '未检测到人脸！请重试……'

                bk_img = np.array(result_img)  # bk_img是cv2格式的图片
                img = QImage(bk_img.data, bk_img.shape[1], bk_img.shape[0], QImage.Format_RGB888)
                self.ui.lb_video1.setPixmap(QPixmap.fromImage(img))  # 将帧数画面显示

                self.ui.lb_C1_Reminder.setText(str_result)  # 设置提示文本的显示
                break

    def Enroll(self):
        self.ui.bt_C1_Open.setEnabled(True)
        self.ui.bt_C1_Enroll.setEnabled(False)
        str_result = ''
        # 获取当前时间，（月和日小于10时，前面不可以有0，才能进行查询，因为数据库里存的就是不带0的。如果将数据库里的存储格式改成有0的，那第四部分数据统计按日期查询是会失败，因为那部分的日期获取是控件传过来的，格式就是不带有0的。）
        # now_time = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')#这种写法结果是月和日小于10时前面会有0，，若用%-m/%-d写法会崩溃，只能下面那么写
        now_time = datetime.datetime.now().timetuple()#得到的是结构体，形如time.struct_time(tm_year=2017, tm_mon=3, tm_mday=24, tm_hour=19, tm_min=37, tm_sec=3, tm_wday=4, tm_yday=83, tm_isdst=-1)
        # print(now_time)
        # 获取年月日值
        time_YMD = str(now_time.tm_year) + '/' + str(now_time.tm_mon) + '/' + str(now_time.tm_mday)
        # 对数据库签到表添加数据，并提示签到成功
        if self.rec_num == -1:  # -1表示没能识别出人脸结果
            str_result = '签到失败,请重试！'
        else:
            # 检查今日是否已签过到
            str_sql = "select * " \
                      " from sign_info " \
                      " WHERE num==" + str(self.rec_num) +" and CAST(time AS VARCHAR ) LIKE " + "'" + time_YMD + "%'"
            print(str_sql)
            query = QSqlQuery()
            query.prepare(str_sql)
            item_list = []
            if not query.exec_():
                query.lastError()
            else:
                while query.next():
                    item_list.append('*')
                    break
            if len(item_list) != 0:
                str_result = '您今日已进行过签到，不可重复签到！'

            else:
                isLate = int(now_time.tm_hour)#获取小时值
                state = ''
                if isLate >= 8:#若8点之后才签到，则记为迟到
                    isLate = 1
                    state = '（迟到上班）'
                else:
                    isLate = 0
                    state = '（正常上班）'
                query = QSqlQuery()
                now_time = time_YMD + ' ' + str(now_time.tm_hour) + ':' + str(now_time.tm_min) + ':' + str(now_time.tm_sec)
                # print(now_time)
                insert_sql = "insert into sign_info values ( NULL" + "," + str(self.rec_num) + ",\'" + now_time + "\'," + str(isLate) + ')'
                # print(insert_sql)
                query.prepare(insert_sql)
                if not query.exec_():
                    str_result = '签到失败！'
                    # return
                else:
                    str_result = '签到成功！' + state
        self.rec_num = -1#必须重新将其置为-1，-1表示没能识别出人脸结果
        self.ui.lb_C1_Reminder.setText(str_result)
        self.update_list_C1_DBInfo(time_YMD + '%')  # 对侧栏今日签到信息进行实时更新
        pass

    def update_list_C1_DBInfo(self,time):# 对侧栏今日签到信息进行实时更新
        str_sql = "select worker_info.num,worker_info.name,sign_info.time " \
                  "from sign_info,worker_info " \
                  "WHERE worker_info.num==sign_info.num and CAST(sign_info.time AS VARCHAR ) LIKE " + "'" + time + "'" + "ORDER BY sign_info.time DESC"
        query = QSqlQuery()
        query.prepare(str_sql)
        # print(str_sql)

        # 将查询到的数据放至item_list列表中
        item_list1 = []
        if not query.exec_():
            query.lastError()
        else:
            while query.next():
                id = query.value(0)
                name = query.value(1)
                time = query.value(2)
                item_list1.append(str(id) + '-' + str(name) + '\t' + str(time))

        # print(str_sql)
        self.list_C1_DBInfo.clear()  # 先将list_C1_DBInfo控件内容情况
        # 添加两个空白行
        self.list_C1_DBInfo.addItems([' '])
        self.list_C1_DBInfo.addItems([' '])
        self.list_C1_DBInfo.addItems(['****************************************'])
        if len(item_list1)==0:# 若数据库中无今日数据
            self.list_C1_DBInfo.addItems(['\t暂无数据'])
        else:# 若数据库中有今日数据
            self.list_C1_DBInfo.addItems(['职员\t日期'])
            self.list_C1_DBInfo.addItems(item_list1)