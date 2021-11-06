# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_Dialog_AddStaff.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 400)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 10, 391, 20))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(Form)
        self.line.setGeometry(QtCore.QRect(20, 30, 351, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(60, 70, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(60, 110, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(60, 150, 100, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.input_C12_Num = QtWidgets.QLineEdit(Form)
        self.input_C12_Num.setGeometry(QtCore.QRect(170, 70, 151, 20))
        self.input_C12_Num.setObjectName("input_C12_Num")
        self.input_C12_Name = QtWidgets.QLineEdit(Form)
        self.input_C12_Name.setGeometry(QtCore.QRect(170, 110, 151, 20))
        self.input_C12_Name.setObjectName("input_C12_Name")
        self.bt_C12_ChooseImg = QtWidgets.QPushButton(Form)
        self.bt_C12_ChooseImg.setGeometry(QtCore.QRect(170, 150, 151, 23))
        self.bt_C12_ChooseImg.setObjectName("bt_C12_ChooseImg")
        self.bt_C12_Submit = QtWidgets.QPushButton(Form)
        self.bt_C12_Submit.setGeometry(QtCore.QRect(70, 330, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bt_C12_Submit.setFont(font)
        self.bt_C12_Submit.setObjectName("bt_C12_Submit")
        self.bt_C12_Cancel = QtWidgets.QPushButton(Form)
        self.bt_C12_Cancel.setGeometry(QtCore.QRect(210, 330, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.bt_C12_Cancel.setFont(font)
        self.bt_C12_Cancel.setObjectName("bt_C12_Cancel")
        self.lb_C12_CurrImg = QtWidgets.QLabel(Form)
        self.lb_C12_CurrImg.setGeometry(QtCore.QRect(70, 180, 250, 130))
        self.lb_C12_CurrImg.setAutoFillBackground(True)
        self.lb_C12_CurrImg.setAlignment(QtCore.Qt.AlignCenter)
        self.lb_C12_CurrImg.setObjectName("lb_C12_CurrImg")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "录入新员工"))
        self.label.setText(_translate("Form", "录入新员工"))
        self.label_2.setText(_translate("Form", "设置职工号："))
        self.label_3.setText(_translate("Form", "姓名："))
        self.label_4.setText(_translate("Form", "头像上传："))
        self.bt_C12_ChooseImg.setText(_translate("Form", "选择图片文件"))
        self.bt_C12_Submit.setText(_translate("Form", "提交"))
        self.bt_C12_Cancel.setText(_translate("Form", "取消"))
        self.lb_C12_CurrImg.setText(_translate("Form", "图片预览区"))
