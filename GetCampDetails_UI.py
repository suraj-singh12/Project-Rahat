# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GetCampDetails_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(823, 784)
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(50, 20, 731, 561))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.label_10 = QtWidgets.QLabel(self.splitter)
        self.label_10.setObjectName("label_10")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setHorizontalSpacing(100)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setMinimumSize(QtCore.QSize(0, 30))
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_3)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_4.setMinimumSize(QtCore.QSize(0, 30))
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_4)
        self.label_11 = QtWidgets.QLabel(self.splitter)
        self.label_11.setObjectName("label_11")
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.formLayout_2 = QtWidgets.QFormLayout(self.layoutWidget1)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.formLayout_2.setHorizontalSpacing(60)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_5.setMinimumSize(QtCore.QSize(0, 30))
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_5.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_5.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_5)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_6.setMinimumSize(QtCore.QSize(0, 30))
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_6.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_6.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_6.setText("")
        self.lineEdit_6.setMaxLength(12)
        self.lineEdit_6.setClearButtonEnabled(False)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_6)
        self.label_7 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_7.setMinimumSize(QtCore.QSize(0, 30))
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_7.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_7.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_7)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_8.setMinimumSize(QtCore.QSize(0, 30))
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.lineEdit_8 = QtWidgets.QLineEdit(self.layoutWidget1)
        self.lineEdit_8.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_8.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_8)
        self.label_13 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_13.setMinimumSize(QtCore.QSize(0, 30))
        self.label_13.setObjectName("label_13")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.spinBox_2 = QtWidgets.QSpinBox(self.layoutWidget1)
        self.spinBox_2.setMinimumSize(QtCore.QSize(0, 30))
        self.spinBox_2.setInputMethodHints(QtCore.Qt.ImhNone)
        self.spinBox_2.setMinimum(1)
        self.spinBox_2.setMaximum(20)
        self.spinBox_2.setSingleStep(1)
        self.spinBox_2.setProperty("value", 1)
        self.spinBox_2.setObjectName("spinBox_2")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.spinBox_2)
        self.label_12 = QtWidgets.QLabel(self.splitter)
        self.label_12.setObjectName("label_12")
        self.layoutWidget2 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.formLayout_3 = QtWidgets.QFormLayout(self.layoutWidget2)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.formLayout_3.setHorizontalSpacing(40)
        self.formLayout_3.setObjectName("formLayout_3")
        self.spinBox = QtWidgets.QSpinBox(self.layoutWidget2)
        self.spinBox.setMinimumSize(QtCore.QSize(0, 30))
        self.spinBox.setMinimum(350)
        self.spinBox.setMaximum(1000)
        self.spinBox.setSingleStep(25)
        self.spinBox.setObjectName("spinBox")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBox)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_9.setMinimumSize(QtCore.QSize(0, 30))
        self.label_9.setObjectName("label_9")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.splitter_2 = QtWidgets.QSplitter(Dialog)
        self.splitter_2.setGeometry(QtCore.QRect(560, 700, 221, 41))
        self.splitter_2.setMinimumSize(QtCore.QSize(0, 0))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.pushButton = QtWidgets.QPushButton(self.splitter_2)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.splitter_2)
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(Dialog)
        self.pushButton_2.clicked.connect(self.spinBox.clear) # type: ignore
        self.pushButton_2.clicked.connect(self.lineEdit_8.clear) # type: ignore
        self.pushButton_2.clicked.connect(self.lineEdit_7.clear) # type: ignore
        self.pushButton_2.clicked.connect(self.lineEdit_6.clear) # type: ignore
        self.pushButton_2.clicked.connect(self.lineEdit_5.clear) # type: ignore
        self.pushButton_2.clicked.connect(self.lineEdit_4.clear) # type: ignore
        self.pushButton_2.clicked.connect(self.lineEdit_3.clear) # type: ignore
        self.pushButton_2.clicked.connect(self.lineEdit_2.clear) # type: ignore
        self.pushButton_2.clicked.connect(self.lineEdit.clear) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_10.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Location Details:</span></p></body></html>"))
        self.label.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">State</span></p></body></html>"))
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">District</span></p></body></html>"))
        self.label_3.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">City/Village</span></p></body></html>"))
        self.label_4.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Coordinates</span></p></body></html>"))
        self.label_11.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Camp Admin Details:</span></p></body></html>"))
        self.label_5.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Admin Name</span></p></body></html>"))
        self.label_6.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Admin Aadhar</span></p></body></html>"))
        self.label_7.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Email Address</span></p></body></html>"))
        self.label_8.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Phone Number</span></p></body></html>"))
        self.label_13.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Support Members</span></p></body></html>"))
        self.label_12.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Camp Related:</span></p></body></html>"))
        self.label_9.setText(_translate("Dialog", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Total Camp Capacity</span></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Submit"))
        self.pushButton_2.setText(_translate("Dialog", "Reset"))
