from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

# 绘制柱状图
class MainWindows(QWidget):
    def __init__(self):
        super(MainWindows, self).__init__()
        self.resize(700,500)

    def paintEvent(self, QPaintEvent):
        X = [1, 2, 3, 4, 5, 6]
        Y = [[141, 400, 700, 460], [120, 50, 340, 55], [141, 400, 700, 460], [120, 50, 340, 55], [120, 50, 340, 55],
             [141, 400, 700, 460]]


        painter = QPainter()
        painter.begin(self)
        painter.setPen(Qt.NoPen)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        pointx = 35
        pointy = self.height() - 50

        width = self.width() - 150 - pointx
        height = self.height()
        # X轴
        painter.drawLine(pointx, pointy, width + pointx, pointy)
        # Y轴
        painter.drawLine(pointx, pointy - height, pointx, pointy)

        X_Spacing = width / len(X)
        X_little_Spacing = width / len(X) / (len(Y[1]) + 1)

        Y_Spacing = height / len(Y)

        pen = QPen(Qt.red, 5, Qt.SolidLine)
        painter.setPen(pen)
        X_start = X_little_Spacing * 3 + 35
        X_pox = []
        for i in range(len(X)):
            painter.drawPoint(X_start - X_little_Spacing * 2, pointy)
            painter.drawPoint(X_start - X_little_Spacing, pointy)
            painter.drawPoint(X_start, pointy)
            painter.drawPoint(X_start + X_little_Spacing * 2, pointy)
            painter.drawPoint(X_start + X_little_Spacing, pointy)
            painter.drawText(X_start - 15, pointy + 20, str(X[i]))
            X_pox.append(X_start)

            X_start = X_start + X_Spacing
        # print(X_pox)
        Y_max = 0
        for i in range(len(Y)):
            if Y_max < max(Y[i]):
                Y_max = max(Y[i])
        num_Spacing = int(Y_max / (len(Y) - 1)) + 1

        num_start = 0
        Y_start_pox = 0
        end_Pox = 0
        for i in range(len(Y)):
            painter.drawPoint(35, pointy - Y_start_pox)
            end_Pox = pointy - Y_start_pox
            painter.drawText(pointx - 30, pointy - Y_start_pox + 5, str(num_start))
            Y_start_pox = Y_start_pox + Y_Spacing
            num_start = num_start + num_Spacing
        every_pox = (pointy - end_Pox) / (num_start - num_Spacing)

        pen = QPen(Qt.black, 1, Qt.SolidLine)
        painter.setPen(pen)
        print(X_pox)
        for i in range(len(X)):
            brush = QBrush(Qt.Dense1Pattern)
            painter.setBrush(brush)
            painter.drawText(X_pox[i] - X_little_Spacing * 2, pointy - Y[i][0] * every_pox - 5, str(Y[i][0]))
            painter.drawRect(X_pox[i] - X_little_Spacing * 2, pointy - Y[i][0] * every_pox, X_little_Spacing,
                             Y[i][0] * every_pox)
            brush = QBrush(Qt.DiagCrossPattern)
            painter.setBrush(brush)
            painter.drawText(X_pox[i] - X_little_Spacing, pointy - Y[i][1] * every_pox - 5, str(Y[i][1]))
            painter.drawRect(X_pox[i] - X_little_Spacing, pointy - Y[i][1] * every_pox, X_little_Spacing,
                             Y[i][1] * every_pox)
            brush = QBrush(Qt.Dense2Pattern)
            painter.setBrush(brush)
            painter.drawText(X_pox[i], pointy - Y[i][2] * every_pox - 5, str(Y[i][2]))
            painter.drawRect(X_pox[i], pointy - Y[i][2] * every_pox, X_little_Spacing, Y[i][2] * every_pox)
            brush = QBrush(Qt.Dense3Pattern)
            painter.setBrush(brush)
            painter.drawText(X_pox[i] + X_little_Spacing, pointy - Y[i][3] * every_pox - 5, str(Y[i][3]))
            painter.drawRect(X_pox[i] + X_little_Spacing, pointy - Y[i][3] * every_pox, X_little_Spacing,
                             Y[i][3] * every_pox)

        brush = QBrush(Qt.Dense1Pattern)
        painter.setBrush(brush)
        painter.drawRect(self.width() - 140, 10, 50, 20)
        painter.drawText(self.width() - 80, 25, "Dense1Pattern")

        brush = QBrush(Qt.DiagCrossPattern)
        painter.setBrush(brush)
        painter.drawRect(self.width() - 140, 35, 50, 20)
        painter.drawText(self.width() - 80, 50, "DiagCrossPattern")

        brush = QBrush(Qt.Dense2Pattern)
        painter.setBrush(brush)
        painter.drawRect(self.width() - 140, 60, 50, 20)
        painter.drawText(self.width() - 80, 75, "Dense2Pattern")

        brush = QBrush(Qt.Dense3Pattern)
        painter.setBrush(brush)
        painter.drawRect(self.width() - 140, 85, 50, 20)
        painter.drawText(self.width() - 80, 100, "Dense3Pattern")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWindows()
    demo.show()
    sys.exit(app.exec_())
