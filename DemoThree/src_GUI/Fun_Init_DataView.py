import sys

from PyQt5.QtSql import QSqlDatabase,QSqlQuery
from PyQt5 import QtGui,QtCore,QtSql,QtWidgets
from PyQt5.QtCore import QFile,QDate

class C_Init_DataView:
    def __init__(self, ui, mainWnd):
        self.ui = ui
        self.mainWnd = mainWnd

        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("./ext/db/mydb.db")
        self.db.open()

        self.list_C1_DBInfo = ui.list_C1_DBInfo
        self.list_C41_DBInfo = ui.list_C41_DBInfo
        self.list_C2_DBInfo = ui.list_C2_DBInfo
        self.list_C42_DBInfo = ui.list_C42_DBInfo
        # ui.bt_ViewData.clicked.connect(self.update)

        # 初始化签到信息
        # 以当前时间为关键字进行模糊查询
        curr_time = QDate.currentDate().toString('yyyy/M/d')+'%' # 获取当前时间
        str_sql = "select worker_info.num,worker_info.name,sign_info.time " \
                  "from sign_info,worker_info " \
                  "WHERE worker_info.num==sign_info.num and CAST(sign_info.time AS VARCHAR ) LIKE " + "'" + curr_time + "'" + "ORDER BY sign_info.time DESC"
        query = QSqlQuery()
        query.prepare(str_sql)
        # print(str_sql)

        # 将查询到的数据放至item_list列表中
        item_list1 = []
        item_list4 = []
        if not query.exec_():
            query.lastError()
        else:
            while query.next():
                id = query.value(0)
                name = query.value(1)
                time = query.value(2)
                item_list1.append(str(id) + '-' + str(name) + '\t' + str(time))
                item_list4.append(str(id) + '\t' + str(name) + '\t' + str(time))

        self.list_C1_DBInfo.clear() # 先将list_C1_DBInfo控件内容情况
        # 添加两个空白行
        self.list_C1_DBInfo.addItems([' '])
        self.list_C1_DBInfo.addItems([' '])
        self.list_C1_DBInfo.addItems(['****************************************'])

        self.list_C41_DBInfo.clear()  # 先将list_C41_DBInfo内容清空
        self.list_C41_DBInfo.addItems(['\t今日签到信息统计情况'])
        self.list_C41_DBInfo.addItems(['**********************************************************'])

        if len(item_list1)==0:# 若数据库中无今日数据
            self.list_C1_DBInfo.addItems(['\t暂无数据'])
            self.list_C41_DBInfo.addItems(['暂无数据~'])
        else:# 若数据库中有今日数据
            self.list_C1_DBInfo.addItems(['职员\t日期'])
            self.list_C1_DBInfo.addItems(item_list1)

            self.list_C41_DBInfo.addItems(['职工号\t姓名\t日期'])
            self.list_C41_DBInfo.addItems(item_list4)

        # print(item_list)

        # 初始化违规信息
        # 以当前时间为关键字进行模糊查询
        curr_time = QDate.currentDate().toString('yyyy/M/d') + '%'  # 获取当前时间
        str_sql = "select worker_info.num,worker_info.name,violation_info.time " \
                  "from violation_info,worker_info " \
                  "WHERE worker_info.num==violation_info.num and CAST(violation_info.time AS VARCHAR ) LIKE " + "'" + curr_time + "'" + " ORDER BY violation_info.time DESC"
        query = QSqlQuery()
        query.prepare(str_sql)
        # print(str_sql)

        # 将查询到的数据放至item_list列表中
        item_list1 = []
        item_list4 = []
        if not query.exec_():
            query.lastError()
        else:
            while query.next():
                id = query.value(0)
                name = query.value(1)
                time = query.value(2)
                item_list1.append(str(id) + '-' + str(name) + '\t' + str(time))
                item_list4.append(str(id) + '\t' + str(name) + '\t' + str(time))

        self.list_C2_DBInfo.clear()  # 先将list_C2_DBInfo控件内容情况
        # 添加两个空白行
        self.list_C2_DBInfo.addItems([' '])
        self.list_C2_DBInfo.addItems([' '])
        self.list_C2_DBInfo.addItems(['****************************************'])

        self.list_C42_DBInfo.clear()  # 先将list_C42_DBInfo内容清空
        self.list_C42_DBInfo.addItems(['\t今日违规信息统计情况'])
        self.list_C42_DBInfo.addItems(['**********************************************************'])

        if len(item_list1) == 0:  # 若数据库中无今日数据
            self.list_C2_DBInfo.addItems(['\t暂无数据'])
            self.list_C42_DBInfo.addItems(['暂无数据~'])
        else:  # 若数据库中有今日数据
            self.list_C2_DBInfo.addItems(['职员\t日期'])
            self.list_C2_DBInfo.addItems(item_list1)

            self.list_C42_DBInfo.addItems(['职工号\t姓名\t日期'])
            self.list_C42_DBInfo.addItems(item_list4)
