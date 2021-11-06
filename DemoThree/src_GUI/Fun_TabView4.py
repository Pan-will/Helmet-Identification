import cv2
import threading
from PyQt5.QtCore import QFile,QDate
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtSql import QSqlDatabase,QSqlQuery
import numpy as np
from PIL import ImageDraw,ImageFont,Image
from timeit import default_timer as timer
import math

class C_DisPlay_Tab4:
    def __init__(self, ui, mainWnd):
        self.ui = ui
        self.mainWnd = mainWnd
        self.tabView = 4

        # 设置查询的日期默认为当前时间
        self.ui.input_C41_Date.setDate(QDate.currentDate())
        self.ui.input_C41_Date_Late.setDate(QDate.currentDate())
        self.ui.input_C42_Date.setDate(QDate.currentDate())

        # self.db = QSqlDatabase.addDatabase("QSQLITE")
        # self.db.setDatabaseName("./ext/db/mydb.db")
        # self.db.open()

        # 信号槽设置
        ui.bt_C41_searchDate.clicked.connect(self.Search_Sign_byData)
        ui.bt_C41_searchNum.clicked.connect(self.Search_Sign_byNum)
        ui.bt_C41_searchDate_Late.clicked.connect(self.Search_Late_byData)
        ui.bt_C41_searchNum_Late.clicked.connect(self.Search_Late_byNum)
        ui.bt_C42_searchDate.clicked.connect(self.Search_Violation_byData)
        ui.bt_C42_searchNum.clicked.connect(self.Search_Violation_byNum)
        #
        # # self.ui.bt_C2_Work.setEnabled(True)
        # self.ui.bt_C3_Close.setEnabled(False)
        #
        # 创建一个关闭事件并设为未触发
        self.stopEvent = threading.Event()
        self.stopEvent.clear()


    def Search_Sign_byData(self):
        # print('测试链接成功')
        key_data = self.ui.input_C41_Date.text()
        result = self.Search_result(page=0,key=key_data, type=2)
        self.Update_C41_DBInfo(result,1)    # 1表示签到查询


    def Search_Sign_byNum(self):
        key_num = self.ui.input_C41_Num.text()
        result = self.Search_result(page=0,key=key_num,type=1)
        self.Update_C41_DBInfo(result,1)    # 1表示签到查询

    def Search_Late_byData(self):
        # print('测试链接成功')
        key_data = self.ui.input_C41_Date_Late.text()
        result = self.Search_result(page=1,key=key_data, type=2)
        self.Update_C41_DBInfo(result,2)    # 1表示迟到查询


    def Search_Late_byNum(self):
        key_num = self.ui.input_C41_Num_Late.text()
        result = self.Search_result(page=1,key=key_num,type=1)
        self.Update_C41_DBInfo(result,2)    # 1表示迟到查询

    def Search_Violation_byData(self):
        # print('测试链接成功')
        key_data = self.ui.input_C42_Date.text()
        result = self.Search_result(page=2,key=key_data, type=2)
        self.Update_C42_DBInfo(result)
        # print()


    def Search_Violation_byNum(self):
        key_num = self.ui.input_C42_Num.text()
        result = self.Search_result(page=2,key=key_num,type=1)
        self.Update_C42_DBInfo(result)

    def Update_C41_DBInfo(self,result,type):
        if type == 1:   # 查询签到信息
            self.ui.list_C41_DBInfo.clear()
            self.ui.list_C41_DBInfo.addItems(['\t所查签到信息统计情况'])
            self.ui.list_C41_DBInfo.addItems(['**********************************************************'])
            if len(result)==0:
                self.ui.list_C41_DBInfo.addItems(['暂无数据~'])
            else:
                self.ui.list_C41_DBInfo.addItems(['职工号\t姓名\t日期'])
                self.ui.list_C41_DBInfo.addItems(result)
        else:   # 查询迟到信息
            self.ui.list_C41_DBInfo.clear()
            self.ui.list_C41_DBInfo.addItems(['\t所查迟到信息统计情况'])
            self.ui.list_C41_DBInfo.addItems(['**********************************************************'])
            if len(result) == 0:
                self.ui.list_C41_DBInfo.addItems(['暂无数据~'])
            else:
                self.ui.list_C41_DBInfo.addItems(['职工号\t姓名\t日期'])
                self.ui.list_C41_DBInfo.addItems(result)


    def Update_C42_DBInfo(self, result):
        if len(result) == 0:
            self.ui.list_C42_DBInfo.clear()
            self.ui.list_C42_DBInfo.addItems(['\t所查违规信息统计情况'])
            self.ui.list_C42_DBInfo.addItems(['**********************************************************'])
            self.ui.list_C42_DBInfo.addItems(['暂无数据~'])
        else:
            self.ui.list_C42_DBInfo.clear()
            self.ui.list_C42_DBInfo.addItems(['\t所查违规信息统计情况'])
            self.ui.list_C42_DBInfo.addItems(['**********************************************************'])
            self.ui.list_C42_DBInfo.addItems(['职工号\t姓名\t日期'])
            self.ui.list_C42_DBInfo.addItems(result)

    def Search_result(self,page,key,type):#page=0是签到查询，page=1是迟到查询，page=2是违规查询，type=1是文本查询，type=2是日期查询，
        str_sql = ''
        if key=='':
            return []
        if page==0:#签到信息查询
            if type == 1:# 按职工号精确查询
                key_num = key  # 按职工号精确查询
                str_sql = "select worker_info.num,worker_info.name,sign_info.time " \
                          " from sign_info,worker_info " \
                          " WHERE worker_info.num==sign_info.num and worker_info.num ==" + key_num + \
                          " ORDER BY sign_info.time DESC"
            else:# 按日期模糊查询
                key_time = key + '%'  # 按日期模糊查询
                str_sql = "select worker_info.num,worker_info.name,sign_info.time " \
                          "from sign_info,worker_info " \
                          "WHERE worker_info.num==sign_info.num and CAST(sign_info.time AS VARCHAR ) LIKE " + "'" + key_time + "'" + \
                          " ORDER BY sign_info.time DESC"
        elif page==1:#迟到信息查询
            if type == 1:# 按职工号精确查询
                key_num = key  # 按职工号精确查询
                str_sql = "select worker_info.num,worker_info.name,sign_info.time " \
                          " from sign_info,worker_info " \
                          " WHERE worker_info.num==sign_info.num and sign_info.isLate==1 and worker_info.num ==" + key_num + \
                          " ORDER BY sign_info.time DESC"
            else:# 按日期模糊查询
                key_time = key + '%'  # 按日期模糊查询
                str_sql = "select worker_info.num,worker_info.name,sign_info.time " \
                          "from sign_info,worker_info " \
                          "WHERE worker_info.num==sign_info.num and sign_info.isLate==1 and CAST(sign_info.time AS VARCHAR ) LIKE " + "'" + key_time + "'" + \
                          " ORDER BY sign_info.time DESC"
        else:#违规信息查询
            if type == 1:# 按职工号精确查询
                key_num = key   # 按职工号精确查询
                str_sql = "select worker_info.num,worker_info.name,violation_info.time " \
                          " from violation_info,worker_info " \
                          " WHERE worker_info.num==violation_info.num and worker_info.num ==" + key_num + \
                          " ORDER BY violation_info.time DESC"
            else:# 按日期模糊查询
                key_time = key + '%'  # 按日期模糊查询
                str_sql = "select worker_info.num,worker_info.name,violation_info.time " \
                          " from violation_info,worker_info " \
                          " WHERE worker_info.num==violation_info.num and CAST(violation_info.time AS VARCHAR ) LIKE " + "'" + key_time + "'" + \
                          " ORDER BY violation_info.time DESC"
        # print(str_sql)
        # print(page,key,type)
        query = QSqlQuery()
        query.prepare(str_sql)
        item_list = []

        if not query.exec_():
            query.lastError()
        else:
            while query.next():
                id = query.value(0)
                name = query.value(1)
                time = query.value(2)
                item_list.append(str(id) + '\t' + str(name) + '\t' + str(time))
        return item_list
