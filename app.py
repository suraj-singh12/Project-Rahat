import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from portal_window import Ui_mainWindow
from Database import Database
from SysAdmin import SysAdmin
from CampAdmin import CampAdmin
from sys_admin_window import Ui_SysAdminWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("RAHAT V1.0")
        # self.setFixedSize(QSize(1000, 700))
        # self.showMaximized()
        self.button = QPushButton("Click Me...")
        # self.button.clicked.connect(self.button_is_clicked)
        # self.button.click()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)
        # self.show()

    # def button_is_clicked(self):
    #     # self.hide()
    #     self.portal_1 = Portal()
    #     self.portal_1.show()


class SysAdminWindow(QMainWindow, Ui_SysAdminWindow):
    def __init__(self):
        super(SysAdminWindow, self).__init__()
        self.setupUi(self)


class Portal(QMainWindow, Ui_mainWindow):

    def __init__(self):
        super(Portal, self).__init__()
        self.setupUi(self)
        self.pushButton.setEnabled(False)

        self.lineEdit.setEnabled(False)
        self.lineEdit_2.setEnabled(False)
        self.show()

    def combo_box_index_changed(self, index):
        # for campAdmin (camp name box)
        if index == 2:
            self.lineEdit.setEnabled(True)
        else:
            self.lineEdit.setEnabled(False)

        # for password and connect button (until an option is selected, password field and connect button are disabled)
        if index == 0:
            self.lineEdit_2.setEnabled(False)
            self.pushButton.setEnabled(False)
        else:
            self.lineEdit_2.setEnabled(True)
            self.pushButton.setEnabled(True)

    def connect_clicked(self):
        print("Connect")
        which_portal = self.comboBox.currentIndex()
        pswd = self.lineEdit_2.text()
        print(which_portal, pswd)

        if which_portal == 1:
            admin = SysAdmin(pswd)
            print("reached admin object created")
            # if the password is correct, program will proceed else it exits at this point
            self.win = SysAdminWindow()
            self.win.showMaximized()
            self.close()



    def reset_clicked(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.comboBox.setCurrentIndex(0)
        print("Reset")


app = QApplication(sys.argv)
window = Portal()
app.exec()
