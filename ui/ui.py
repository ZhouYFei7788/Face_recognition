# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Initialize buttons and labels
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(110, 600, 140, 40))
        font = QtGui.QFont()
        font.setFamily("Algerian")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 720, 480))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setLineWidth(3)
        self.label.setText("")
        self.label.setObjectName("label")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(350, 600, 140, 40))
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(770, 20, 220, 480))
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(770, 20, 220, 30))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(770, 60, 220, 240))
        self.label_4.setFrameShape(QtWidgets.QFrame.Box)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(780, 330, 60, 30))
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(850, 330, 120, 30))
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(780, 400, 60, 30))
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(850, 405, 130, 25))
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(850, 405, 130, 25))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(620, 530, 371, 151))
        self.label_9.setFrameShape(QtWidgets.QFrame.Box)
        self.label_9.setLineWidth(2)
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(640, 540, 161, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(640, 610, 161, 51))
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")

        self.yn = QtWidgets.QLabel(self.centralwidget)
        self.yn.setGeometry(QtCore.QRect(820, 550, 121, 31))
        self.yn.setText("")
        self.yn.setObjectName("yn")

        self.YN = QtWidgets.QLabel(self.centralwidget)
        self.YN.setGeometry(QtCore.QRect(820, 620, 121, 31))
        self.YN.setText("")
        self.YN.setObjectName("YN")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "人脸识别与眨眼检测"))
        self.pushButton.setText(_translate("MainWindow", "打开摄像头"))
        self.pushButton_3.setText(_translate("MainWindow", "开始识别"))
        self.label_3.setText(_translate("MainWindow", "识别结果："))
        self.label_5.setText(_translate("MainWindow", "姓名："))
        self.label_7.setText(_translate("MainWindow", "准确率："))
        self.pushButton_2.setText(_translate("MainWindow", "眨眼"))
        self.pushButton_4.setText(_translate("MainWindow", "张嘴"))