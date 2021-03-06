# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RequestSupply_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RequestSupplyPopup(object):
    def setupUi(self, RequestSupplyPopup):
        RequestSupplyPopup.setObjectName("RequestSupplyPopup")
        RequestSupplyPopup.resize(654, 326)
        self.layoutWidget = QtWidgets.QWidget(RequestSupplyPopup)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 70, 571, 143))
        self.layoutWidget.setObjectName("layoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setHorizontalSpacing(50)
        self.formLayout.setObjectName("formLayout")
        self.item_name_label = QtWidgets.QLabel(self.layoutWidget)
        self.item_name_label.setMinimumSize(QtCore.QSize(0, 30))
        self.item_name_label.setObjectName("item_name_label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.item_name_label)
        self.lineEdit_item_name = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_item_name.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_item_name.setObjectName("lineEdit_item_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_item_name)
        self.item_type_label = QtWidgets.QLabel(self.layoutWidget)
        self.item_type_label.setMinimumSize(QtCore.QSize(0, 30))
        self.item_type_label.setObjectName("item_type_label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.item_type_label)
        self.comboBox_item_type = QtWidgets.QComboBox(self.layoutWidget)
        self.comboBox_item_type.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox_item_type.setObjectName("comboBox_item_type")
        self.comboBox_item_type.addItem("")
        self.comboBox_item_type.addItem("")
        self.comboBox_item_type.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBox_item_type)
        self.item_description_label = QtWidgets.QLabel(self.layoutWidget)
        self.item_description_label.setMinimumSize(QtCore.QSize(0, 30))
        self.item_description_label.setObjectName("item_description_label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.item_description_label)
        self.lineEdit_item_desc = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_item_desc.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_item_desc.setObjectName("lineEdit_item_desc")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_item_desc)
        self.quantity_label = QtWidgets.QLabel(self.layoutWidget)
        self.quantity_label.setMinimumSize(QtCore.QSize(0, 30))
        self.quantity_label.setObjectName("quantity_label")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.quantity_label)
        self.spinbox_quantity = QtWidgets.QSpinBox(self.layoutWidget)
        self.spinbox_quantity.setMinimumSize(QtCore.QSize(0, 30))
        self.spinbox_quantity.setMaximum(1000)
        self.spinbox_quantity.setObjectName("spinbox_quantity")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spinbox_quantity)
        self.layoutWidget1 = QtWidgets.QWidget(RequestSupplyPopup)
        self.layoutWidget1.setGeometry(QtCore.QRect(420, 240, 211, 42))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_submit = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_submit.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.horizontalLayout.addWidget(self.pushButton_submit)
        self.pushButton_reset = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushButton_reset.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.horizontalLayout.addWidget(self.pushButton_reset)
        self.label_5 = QtWidgets.QLabel(RequestSupplyPopup)
        self.label_5.setGeometry(QtCore.QRect(50, 20, 161, 31))
        self.label_5.setObjectName("label_5")
        self.line = QtWidgets.QFrame(RequestSupplyPopup)
        self.line.setGeometry(QtCore.QRect(60, 50, 571, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.retranslateUi(RequestSupplyPopup)
        QtCore.QMetaObject.connectSlotsByName(RequestSupplyPopup)

    def retranslateUi(self, RequestSupplyPopup):
        _translate = QtCore.QCoreApplication.translate
        RequestSupplyPopup.setWindowTitle(_translate("RequestSupplyPopup", "Dialog"))
        self.item_name_label.setText(_translate("RequestSupplyPopup", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Item Name</span></p></body></html>"))
        self.item_type_label.setText(_translate("RequestSupplyPopup", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Item Type</span></p></body></html>"))
        self.comboBox_item_type.setItemText(0, _translate("RequestSupplyPopup", "Select Type"))
        self.comboBox_item_type.setItemText(1, _translate("RequestSupplyPopup", "Regular"))
        self.comboBox_item_type.setItemText(2, _translate("RequestSupplyPopup", "Medical"))
        self.item_description_label.setText(_translate("RequestSupplyPopup", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Item Description</span></p></body></html>"))
        self.quantity_label.setText(_translate("RequestSupplyPopup", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt;\">Quantity</span></p></body></html>"))
        self.pushButton_submit.setText(_translate("RequestSupplyPopup", "Submit"))
        self.pushButton_reset.setText(_translate("RequestSupplyPopup", "Reset"))
        self.label_5.setText(_translate("RequestSupplyPopup", "<html><head/><body><p align=\"center\"><span style=\" font-size:10pt; font-weight:600;\">Request Supply</span></p></body></html>"))
