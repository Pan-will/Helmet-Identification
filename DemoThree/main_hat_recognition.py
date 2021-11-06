import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from src_GUI.UI_Main import *
from src_GUI.Fun_TabView1 import C_DisPlay_Tab1
from src_GUI.Fun_TabView2 import C_DisPlay_Tab2
from src_GUI.Fun_TabView3C2 import C_DisPlay_Tab3
from src_GUI.Fun_TabView4 import C_DisPlay_Tab4
from src_GUI.Fun_Init_DataView import C_Init_DataView
from src_GUI.UI_Dialog_AddStaff import Ui_Dialog
from src_GUI.UI_Main import Ui_Form

# from yolo import YOLO   # yolov3版本
from yolov3_tiny.yolo_tiny import YOLO  # yolov3_tiny版本
from face_rec.Recognize_From_Photo import Face_Rec

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWnd = QMainWindow()

    MainUI = Ui_Form()
    MainUI.setupUi(mainWnd)

    yolo = YOLO()
    face_rec = Face_Rec()

    display0 = C_Init_DataView(MainUI, mainWnd)
    display1 = C_DisPlay_Tab1(MainUI, mainWnd, yolo, face_rec)
    display2 = C_DisPlay_Tab2(MainUI, mainWnd, yolo, face_rec)
    display3 = C_DisPlay_Tab3(MainUI, mainWnd, yolo)
    display4 = C_DisPlay_Tab4(MainUI, mainWnd)

    mainWnd.show()

    sys.exit(app.exec_())
